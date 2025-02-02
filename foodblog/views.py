from django.shortcuts import render,get_object_or_404, redirect

# Create your views here.
from django.views.generic import TemplateView,ListView, DetailView #表示関連
from django.views import View
import requests, json
from django.db.models import Count, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from .models import Shop, Genre, Station, Favorite, Comment
from .forms import CommentForm


class SideDataMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # サイドバー用データ（カテゴリー、駅）
        context['genres'] = Genre.objects.all()

        # 駅を最大20件取得（最初は20件）
        stations = Station.objects.annotate(shop_count=Count('shop')).order_by('-shop_count')[:20]
        context['stations'] = stations
        all_stations = Station.objects.annotate(shop_count=Count('shop')).filter(~Q(id=180)).order_by('-shop_count')[20:]  # 全ての駅
        context['all_stations_json'] = json.dumps(list(all_stations.values('id', 'name', 'shop_count')))  # 全駅のJSON

        return context

class IndexView(SideDataMixin, ListView):
    # トップページのビュー
    template_name = 'index.html' # index.htmlをレンダリング

    context_object_name = 'shops' # テンプレート内でのオブジェクト名
    queryset = Shop.objects.order_by('?') # Shopモデルのデータを全て取得

    paginate_by = 10 # 1ページに表示する件数

class ShopDetailView(SideDataMixin, DetailView):
    template_name = 'shop_detail.html'

    model = Shop
    context_object_name = 'shop'
    def get_context_data(self, **kwargs):
        # 親クラスのget_context_dataを呼び出して、共通のサイドバー用データを取得
        context = super().get_context_data(**kwargs)

        # 現在のショップ（お店）のオブジェクトを取得
        shop = self.get_object()

        # ユーザーがそのお店をお気に入りにしているかどうかを確認
        is_favorite = Favorite.objects.filter(user=self.request.user, shop=shop).exists() if self.request.user.is_authenticated else False

        # is_favorite をテンプレートに渡す
        context['is_favorite'] = is_favorite

        # comment_formを返す
        context['comment_form'] = CommentForm

        # お店についているコメント
        context['comments'] = Comment.objects.filter(shop=self.object).order_by('-created_at')

        return context
    
    def post(self, request, *args, **kwargs):
        shop = self.get_object()  # 現在のお店を取得
        form = CommentForm(request.POST)
        if form.is_valid():
            # コメントを保存
            comment = form.save(commit=False)
            comment.shop = shop  # 現在のショップに関連付け
            comment.user = request.user  # 現在のユーザーを設定
            comment.save()
            return redirect('foodblog:shop_detail', pk=shop.pk)  # 詳細ページにリダイレクト
        else:
            # フォームが無効ならそのままページを返す
            context = self.get_context_data(form=form)
            return self.render_to_response(context)

class GenreListView(SideDataMixin, ListView):
    template_name = 'index.html' # index.htmlをレンダリング

    context_object_name = 'shops' # テンプレート内でのオブジェクト名
    paginate_by = 10 # 1ページに表示する件数

    def get_queryset(self):
        genre_id = self.kwargs['genre']

        genres = Shop.objects.filter(
            genre = genre_id).order_by('id')
        return genres

class StationListView(SideDataMixin, ListView):
    template_name = 'index.html' # index.htmlをレンダリング

    context_object_name = 'shops' # テンプレート内でのオブジェクト名
    paginate_by = 10 # 1ページに表示する件数

    def get_queryset(self):
        station_id = self.kwargs['station']

        stations = Shop.objects.filter(
            station = station_id).order_by('id')
        return stations

class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, shop_id):
        # お店のインスタンスを取得
        shop = get_object_or_404(Shop, id=shop_id)

        # ユーザーがまだお気に入りにしていない場合に追加
        if not Favorite.objects.filter(user=request.user, shop=shop).exists():
            Favorite.objects.create(user=request.user, shop=shop)

        # お店の詳細ページへリダイレクト
        return redirect('foodblog:shop_detail', pk=shop.id)


class RemoveFavoriteView(LoginRequiredMixin, View):
    def post(self, request, shop_id):
        # お店のインスタンスを取得
        shop = get_object_or_404(Shop, id=shop_id)

        # ユーザーのお気に入りから削除
        favorite = Favorite.objects.filter(user=request.user, shop=shop)
        if favorite.exists():
            favorite.delete()

        # お店の詳細ページへリダイレクト
        return redirect('foodblog:shop_detail', pk=shop.id)

class MypageView(ListView):
    template_name = 'mypage.html'

    context_object_name = 'favorite_shops'

    def get_queryset(self):
        return Shop.objects.filter(favorite__user=self.request.user).order_by('-created_at')

def fetch_and_save_shops():
    API_KEY = '982cfe3c211cb938'
    URL = "https://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
    params = {
        "key": API_KEY,
        "large_area": "Z091",  # 福岡エリア
        "format": "json",
        "order": 4,  # レビュー件数順
        "start": 151,  # 1ページ目から取得
        "count": 50,  # 最大50件取得
        "genre": "G004,G006,G008",  
        #済 5,7,13:500  
        #済 14,16,17:500 
        #済 4,6,8:200

    }

    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()

        data = response.json()

        for shop_data in data['results']['shop']:
            shop_name = shop_data['name']
            genre_name=shop_data['genre']['name']
            station_name=shop_data['station_name']

            genre_obj, created = Genre.objects.get_or_create(name=genre_name)

            station_obj, created = Station.objects.get_or_create(name=station_name)
            # 重複チェック
            if not Shop.objects.filter(name=shop_name).exists():
                Shop.objects.create(
                    name=shop_name,
                    address=shop_data['address'],
                    genre=genre_obj,
                    sub_genre=shop_data['genre']['catch'],
                    access=shop_data['access'],
                    station=station_obj,
                    mobile_url=shop_data['coupon_urls']['sp'],
                    photo_large=shop_data['photo']['pc']['l'],
                    photo_medium=shop_data['photo']['pc']['m'],
                    business_hours=shop_data['open'],
                    catch=shop_data['catch'],
                    middle_area=shop_data['middle_area']['name'],
                )
        print("データ登録が完了しました！")

    except requests.exceptions.RequestException as e:
        print(f"エラー: {str(e)}")


