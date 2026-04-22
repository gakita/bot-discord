import json
import os

OFENSAS_PADRAO = [
    "bunda merda",
    "maldito",
    "zé ruela",
    "inútil",
    "lesado",
    "sem vergonha",
]


def carregar_ofensas(caminho: str) -> list[str]:
    if not os.path.exists(caminho):
        return OFENSAS_PADRAO.copy()
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)
    return dados.get("ofensas", OFENSAS_PADRAO.copy())


def salvar_ofensas(caminho: str, ofensas: list[str]) -> None:
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump({"ofensas": ofensas}, f, ensure_ascii=False, indent=2)


def adicionar_ofensa(caminho: str, nova: str) -> list[str]:
    ofensas = carregar_ofensas(caminho)
    ofensas.append(nova)
    salvar_ofensas(caminho, ofensas)
    return ofensas
