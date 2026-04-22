from dotenv import load_dotenv
load_dotenv()

import os
from imagens_manager import salvar_imagem

PASTA = "imagens"

if __name__ == "__main__":
    if not os.path.exists(PASTA):
        print(f"Pasta '{PASTA}' não encontrada. Crie ela e coloque as imagens dentro.")
        exit(1)

    arquivos = [f for f in os.listdir(PASTA) if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))]

    if not arquivos:
        print("Nenhuma imagem encontrada na pasta.")
        exit(1)

    for nome in arquivos:
        caminho = os.path.join(PASTA, nome)
        with open(caminho, "rb") as f:
            dados = f.read()
        salvar_imagem(nome, dados)
        print(f"✓ {nome}")

    print(f"\n{len(arquivos)} imagem(ns) enviada(s) pro MongoDB.")
