# Register your models here.
from django.contrib import admin
from .models import Shop,Station,Favorite,Comment

# Shopモデルを管理画面に登録
@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'genre', 'station', 'created_at')  # 管理画面で表示する項目
    search_fields = ('name', 'address', 'genre', 'station')  # 検索フィールド

admin.site.register(Station)
admin.site.register(Favorite)
admin.site.register(Comment)