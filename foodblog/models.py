from django.db import models
from accounts.models import CustomUser

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Station(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Shop(models.Model):
    # 店名（ユニーク制約をつけることで重複登録を防ぐ）
    name = models.CharField(max_length=255, unique=True)
    
    # 住所
    address = models.CharField(max_length=255)
    
    # ジャンル
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True, blank=True)
    
    # サブジャンル（任意）
    sub_genre = models.CharField(max_length=100, blank=True, null=True)
    
    # アクセス（例: "博多駅 徒歩5分" など）
    access = models.CharField(max_length=255)
    
    # 最寄り駅
    station = models.ForeignKey(Station, on_delete=models.CASCADE, null=True, blank=True)
    
    # スマホ向けURL
    mobile_url = models.URLField()
    
    # 店舗写真（大サイズ）
    photo_large = models.URLField(blank=True, null=True)  # 任意で空の値を許容
    
    # 店舗写真（中サイズ）
    photo_medium = models.URLField(blank=True, null=True)  # 任意で空の値を許容
    
    # 営業時間
    business_hours = models.CharField(max_length=255, blank=True, null=True)  # 任意で空の値を許容

    catch = models.CharField(max_length=255, blank=True, null=True)  # 任意で空の値を許容

    middle_area = models.CharField(max_length=100, blank=True, null=True)  # 任意で空の値を許容
    
    # データ登録日時
    created_at = models.DateTimeField(auto_now_add=True)

    # ユーザーの評価数
    review_count = models.IntegerField(default=0)

    #評価の総合点
    review_total = models.IntegerField(default=0)

    # モデルオブジェクトを表示するための文字列表現
    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # ユーザー
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)  # お店

    class Meta:
        unique_together = ('user', 'shop')  # ユーザーとお店の組み合わせで一意にする

    def __str__(self):
        return f"{self.user.username} - {self.shop.name}"
    created_at = models.DateTimeField(auto_now_add=True)  # お気に入りに追加した日時

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # コメントしたユーザー
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)  # コメント先のお店
    content = models.TextField()  # コメントの内容
    created_at = models.DateTimeField(auto_now_add=True)  # コメントが投稿された日時

    def __str__(self):
        return f'{self.user.username}のコメント: {self.content[:20]}'