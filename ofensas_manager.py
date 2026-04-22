import os
from pymongo import MongoClient

OFENSAS_PADRAO = [
    "bunda merda",
    "maldito",
    "zé ruela",
    "inútil",
    "lesado",
    "sem vergonha",
]

_client = None


def _get_collection():
    global _client
    if _client is None:
        _client = MongoClient(os.environ["MONGODB_URI"])
    return _client["bot_criolo"]["ofensas"]


def carregar_ofensas() -> list[str]:
    col = _get_collection()
    doc = col.find_one({"_id": "lista"})
    if doc is None:
        col.insert_one({"_id": "lista", "ofensas": OFENSAS_PADRAO.copy()})
        return OFENSAS_PADRAO.copy()
    return doc["ofensas"]


def adicionar_ofensa(nova: str) -> list[str]:
    col = _get_collection()
    col.update_one(
        {"_id": "lista"},
        {"$push": {"ofensas": nova}},
        upsert=True,
    )
    return carregar_ofensas()
