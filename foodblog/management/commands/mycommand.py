from django.core.management.base import BaseCommand
from foodblog.views import fetch_and_save_shops  # 適切な場所に関数をインポート

class Command(BaseCommand):
    help = 'ホットペッパーAPIから店舗情報を取得して登録します'

    def handle(self, *args, **kwargs):
        fetch_and_save_shops()
