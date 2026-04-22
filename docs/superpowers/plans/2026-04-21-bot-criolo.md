# Bot Criolo — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bot Discord que a cada 4 horas menciona todos os membros humanos de um servidor no canal `#comandos` com uma ofensa aleatória, e aceita o comando `/add-ofensa` para expandir a lista.

**Architecture:** O bot usa `discord.py` com `discord.ext.tasks` para o agendamento e `app_commands` para o slash command. A persistência das ofensas é feita em `ofensas.json`. A lógica de manipulação do arquivo JSON é isolada em `ofensas_manager.py` para facilitar testes.

**Tech Stack:** Python 3.11+, discord.py 2.3.x, pytest, Railway (hospedagem)

---

## Pré-requisitos manuais (feitos pelo usuário antes do Task 1)

1. Acessar https://discord.com/developers/applications e criar uma nova Application
2. Na aba **Bot**, clicar em "Add Bot"
3. Em **Privileged Gateway Intents**, habilitar **Server Members Intent**
4. Copiar o Token do bot (guardar com segurança)
5. Em **OAuth2 → URL Generator**, marcar scopes: `bot` e `applications.commands`
6. Em permissions, marcar: `Send Messages`, `Read Message History`, `View Channels`
7. Usar a URL gerada para adicionar o bot ao servidor

---

## Estrutura de arquivos

```
bot-criolo/
├── bot.py                  # ponto de entrada — bot, task e comando
├── ofensas_manager.py      # carregar/salvar/adicionar ofensas no JSON
├── config.py               # constantes (canal, arquivo, intervalo)
├── ofensas.json            # lista inicial de ofensas (commitada)
├── requirements.txt        # discord.py, python-dotenv
├── Procfile                # instrução de execução para Railway
├── .env.example            # modelo de variáveis de ambiente
├── .gitignore              # exclui .env e __pycache__
└── tests/
    └── test_ofensas_manager.py
```

---

## Task 1: Scaffolding do projeto

**Files:**
- Create: `config.py`
- Create: `ofensas.json`
- Create: `requirements.txt`
- Create: `.env.example`
- Create: `.gitignore`

- [ ] **Step 1: Criar `config.py`**

```python
CANAL_NOME = "comandos"
OFENSAS_FILE = "ofensas.json"
INTERVALO_HORAS = 4
```

- [ ] **Step 2: Criar `ofensas.json`**

```json
{
  "ofensas": [
    "bunda merda",
    "maldito",
    "zé ruela",
    "inútil",
    "lesado",
    "sem vergonha"
  ]
}
```

- [ ] **Step 3: Criar `requirements.txt`**

```
discord.py==2.3.2
python-dotenv==1.0.0
pytest==8.1.1
```

- [ ] **Step 4: Criar `.env.example`**

```
DISCORD_TOKEN=seu_token_aqui
```

- [ ] **Step 5: Criar `.gitignore`**

```
.env
__pycache__/
*.pyc
*.pyo
.pytest_cache/
```

- [ ] **Step 6: Instalar dependências**

```bash
pip install -r requirements.txt
```

Esperado: instalação sem erros.

- [ ] **Step 7: Commit**

```bash
git init
git add config.py ofensas.json requirements.txt .env.example .gitignore
git commit -m "chore: scaffolding inicial do projeto"
```

---

## Task 2: ofensas_manager (TDD)

**Files:**
- Create: `ofensas_manager.py`
- Create: `tests/test_ofensas_manager.py`

- [ ] **Step 1: Criar pasta de testes**

```bash
mkdir tests
touch tests/__init__.py
```

- [ ] **Step 2: Escrever os testes**

Criar `tests/test_ofensas_manager.py`:

```python
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
```

- [ ] **Step 3: Rodar testes para confirmar que falham**

```bash
pytest tests/test_ofensas_manager.py -v
```

Esperado: ERRO — `ModuleNotFoundError: No module named 'ofensas_manager'`

- [ ] **Step 4: Implementar `ofensas_manager.py`**

```python
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
```

- [ ] **Step 5: Rodar testes para confirmar que passam**

```bash
pytest tests/test_ofensas_manager.py -v
```

Esperado: 5 testes PASS.

- [ ] **Step 6: Commit**

```bash
git add ofensas_manager.py tests/
git commit -m "feat: ofensas_manager com testes"
```

---

## Task 3: Bot principal

**Files:**
- Create: `bot.py`

- [ ] **Step 1: Criar `bot.py`**

```python
import os
import random
import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv

from config import CANAL_NOME, OFENSAS_FILE, INTERVALO_HORAS
from ofensas_manager import carregar_ofensas, adicionar_ofensa

load_dotenv()

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@tasks.loop(hours=INTERVALO_HORAS)
async def zoar_membros():
    for guild in bot.guilds:
        canal = discord.utils.get(guild.text_channels, name=CANAL_NOME)
        if canal is None:
            continue
        ofensas = carregar_ofensas(OFENSAS_FILE)
        membros = [m for m in guild.members if not m.bot]
        for membro in membros:
            ofensa = random.choice(ofensas)
            await canal.send(f"{membro.mention} você é um {ofensa}")


@bot.event
async def on_ready():
    await bot.tree.sync()
    if not zoar_membros.is_running():
        zoar_membros.start()
    print(f"Bot conectado como {bot.user}")


@bot.tree.command(name="add-ofensa", description="Adiciona uma nova ofensa à lista")
@app_commands.describe(ofensa="A ofensa a ser adicionada")
async def add_ofensa(interaction: discord.Interaction, ofensa: str):
    adicionar_ofensa(OFENSAS_FILE, ofensa)
    await interaction.response.send_message(f'Ofensa "{ofensa}" adicionada com sucesso!')


if __name__ == "__main__":
    token = os.environ["DISCORD_TOKEN"]
    bot.run(token)
```

- [ ] **Step 2: Criar arquivo `.env` local (não commitado)**

```bash
cp .env.example .env
```

Abrir `.env` e preencher com o token real do bot:
```
DISCORD_TOKEN=cole_o_token_aqui
```

- [ ] **Step 3: Testar o bot localmente**

```bash
python bot.py
```

Esperado no terminal:
```
Bot conectado como NomeDoBot#1234
```

- [ ] **Step 4: Testar o comando `/add-ofensa` no Discord**

No canal `#comandos` do servidor, digitar:
```
/add-ofensa frango assado
```

Esperado: `Ofensa "frango assado" adicionada com sucesso!`

Verificar que `ofensas.json` foi atualizado com a nova ofensa.

- [ ] **Step 5: Commit**

```bash
git add bot.py
git commit -m "feat: bot principal com task agendada e comando slash"
```

---

## Task 4: Deploy no Railway

**Files:**
- Create: `Procfile`

- [ ] **Step 1: Criar `Procfile`**

```
worker: python bot.py
```

- [ ] **Step 2: Commit**

```bash
git add Procfile
git commit -m "chore: Procfile para Railway"
```

- [ ] **Step 3: Criar repositório no GitHub**

```bash
gh repo create bot-criolo --private --source=. --push
```

Ou manualmente: criar repositório privado no GitHub e fazer push.

- [ ] **Step 4: Configurar Railway**

1. Acessar https://railway.app e criar conta gratuita
2. Clicar em **New Project → Deploy from GitHub repo**
3. Selecionar o repositório `bot-criolo`
4. Após o deploy inicial (vai falhar sem o token), ir em **Variables**
5. Adicionar variável: `DISCORD_TOKEN` = (colar o token do bot)
6. Railway vai reiniciar o bot automaticamente

- [ ] **Step 5: Verificar deploy**

Na aba **Logs** do Railway, confirmar:
```
Bot conectado como NomeDoBot#1234
```

O bot está online 24/7 e vai zoar o servidor a cada 4 horas.
