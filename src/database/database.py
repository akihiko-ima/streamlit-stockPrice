import os
from tinydb import TinyDB, Query
from datetime import datetime
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("DB_PATH")


@contextmanager
def open_db():
    """TinyDBのコンテキストマネージャ"""
    db = TinyDB(DB_PATH)
    try:
        yield db
    finally:
        db.close()


def create_file_data(entry: dict):
    """新しいエントリを追加する"""
    with open_db() as db:
        db.insert(entry)


def get_all_file_data():
    """すべてのエントリを取得する"""
    with open_db() as db:
        return db.all()


def get_file_data_by_id(record_id: int):
    """IDをキーにデータを取得する関数"""
    query = Query()
    with open_db() as db:
        result = db.get(query.id == record_id)
        return result


def delete_file_data(record_id: int):
    """指定されたIDのエントリを削除する"""
    query = Query()
    with open_db() as db:
        db.remove(query.id == record_id)


def clear_db():
    with open_db() as db:
        db.truncate()
