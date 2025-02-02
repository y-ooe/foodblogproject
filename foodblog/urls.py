from django.urls import path
from . import views


app_name = 'foodblog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    
    path('shop-detail/<int:pk>', views.ShopDetailView.as_view(), name='shop_detail'),
    
    path('shop-detail/<int:shop_id>/add-favorite/', views.AddFavoriteView.as_view(), name='add_favorite'),
    path('shop-detail/<int:shop_id>/remove-favorite/', views.RemoveFavoriteView.as_view(), name='remove_favorite'),

    path('genre-list/<int:genre>', views.GenreListView.as_view(), name='genre_list'),
    path('station-list/<int:station>', views.StationListView.as_view(),name='station_list'),
    path('mypage/', views.MypageView.as_view(), name='mypage'),

    path('search/', views.SearchShopView.as_view(), name='search'),

]