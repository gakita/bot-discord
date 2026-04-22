# Ranking dos Zoados + Zoar Alvo — Design Spec

**Data:** 2026-04-22

## Visão Geral

Duas novas funcionalidades para o bot:
1. **Ranking dos zoados** — placar estilizado com emojis de porco mostrando quem foi mais zoado
2. **`/zoar-alvo`** — zoar um membro específico em vez de aleatório

## Armazenamento

Nova coleção MongoDB `zoados` com um documento por usuário zoado:

```json
{"user_id": 123456, "username": "Pedro", "count": 5}
```

Toda zoação (manual, alvo ou automática) incrementa o contador do membro atingido.

## Ranking

Comando `/ranking-zoados` exibe a lista ordenada por contagem decrescente:

```
🐷🐷🐷 RANKING DOS ZOADOS 🐷🐷🐷

🥇 1. @Pedro — 12 zoações 🐽
🥈 2. @Carlos — 8 zoações 🐷
🥉 3. @Cleber — 5 zoações 🐷
4. @Bunda — 2 zoações 🐖
...

🐷 Total de zoações no servidor: 27 🐷
```

- Contagem inclui todas as origens: `/zoar`, `/zoar-alvo` e task automática das 4h
- Emojis de porco variados: 🐷 🐽 🐖
- Visível para todos no canal

## Zoar Alvo

Comando `/zoar-alvo @usuario`:
- Aceita qualquer membro como alvo (sem restrições)
- Comportamento idêntico ao `/zoar`: ofensa aleatória + imagem aleatória
- Conta para o ranking do membro alvo

## Novo arquivo

- `ranking_manager.py` — funções para registrar e consultar o ranking no MongoDB

## Mudanças em arquivos existentes

- `bot.py` — adicionar `/zoar-alvo` e `/ranking-zoados`, atualizar todas as zoações para registrar no ranking
