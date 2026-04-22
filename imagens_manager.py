import io
import os
import random
import gridfs
from pymongo import MongoClient

_client = None


def _get_fs():
    global _client
    if _client is None:
        _client = MongoClient(os.environ["MONGODB_URI"])
    return gridfs.GridFS(_client["bot_criolo"])


def salvar_imagem(nome: str, dados: bytes) -> None:
    fs = _get_fs()
    if not fs.exists({"filename": nome}):
        fs.put(dados, filename=nome)


def carregar_imagem_aleatoria() -> tuple[bytes, str] | None:
    fs = _get_fs()
    arquivos = list(fs.find())
    if not arquivos:
        return None
    arquivo = random.choice(arquivos)
    return arquivo.read(), arquivo.filename


def listar_imagens() -> list[str]:
    fs = _get_fs()
    return [f.filename for f in fs.find()]
