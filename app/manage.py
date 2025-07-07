#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Django の管理タスクを実行"""
    # 使用する設定ファイルを指定　ここを自分のプロジェクト名に合わせる
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django をインポートできませんでした。Django がインストールされていて、 "
            "PYTHONPATH 環境変数に正しく設定されているか確認してください。"
            "仮想環境の有効化を忘れていませんか？"
        ) from exc
    # コマンドライン引数を使って Django のコマンドを実行
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

