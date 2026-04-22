import json
import pytest
from ofensas_manager import carregar_ofensas, salvar_ofensas, adicionar_ofensa, OFENSAS_PADRAO


def test_carregar_ofensas_arquivo_inexistente(tmp_path):
    caminho = str(tmp_path / "nao_existe.json")
    resultado = carregar_ofensas(caminho)
    assert resultado == OFENSAS_PADRAO


def test_carregar_ofensas_arquivo_existente(tmp_path):
    caminho = str(tmp_path / "ofensas.json")
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump({"ofensas": ["lesado", "inútil"]}, f)
    resultado = carregar_ofensas(caminho)
    assert resultado == ["lesado", "inútil"]


def test_salvar_ofensas(tmp_path):
    caminho = str(tmp_path / "ofensas.json")
    salvar_ofensas(caminho, ["bunda", "zé ruela"])
    with open(caminho, encoding="utf-8") as f:
        dados = json.load(f)
    assert dados == {"ofensas": ["bunda", "zé ruela"]}


def test_adicionar_ofensa_nova(tmp_path):
    caminho = str(tmp_path / "ofensas.json")
    adicionar_ofensa(caminho, "frango assado")
    resultado = carregar_ofensas(caminho)
    assert "frango assado" in resultado


def test_adicionar_ofensa_preserva_existentes(tmp_path):
    caminho = str(tmp_path / "ofensas.json")
    salvar_ofensas(caminho, ["lesado"])
    adicionar_ofensa(caminho, "inútil")
    resultado = carregar_ofensas(caminho)
    assert "lesado" in resultado
    assert "inútil" in resultado
