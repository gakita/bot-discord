import os
from pymongo import MongoClient

_client = None


def _get_collection():
    global _client
    if _client is None:
        _client = MongoClient(os.environ["MONGODB_URI"])
    return _client["bot_criolo"]["zoados"]


def registrar_zoacao(user_id: int, username: str) -> None:
    col = _get_collection()
    col.update_one(
        {"user_id": user_id},
        {"$inc": {"count": 1}, "$set": {"username": username}},
        upsert=True,
    )


def carregar_ranking() -> list[dict]:
    col = _get_collection()
    return list(col.find().sort("count", -1))
