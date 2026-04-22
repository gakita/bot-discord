# Bot Criolo — Design Spec

**Data:** 2026-04-21

## Visão Geral

Bot de Discord que a cada 4 horas busca todos os membros humanos de um servidor e envia uma mensagem no canal `#comandos` mencionando cada um com uma ofensa aleatória. A lista de ofensas começa com valores padrão e pode ser expandida via comando slash.

## Arquitetura

```
bot-criolo/
├── bot.py              # ponto de entrada — inicializa o bot e registra comandos/tasks
├── tasks.py            # tarefa agendada a cada 4 horas (discord.ext.tasks)
├── commands.py         # comando slash /add-ofensa
├── ofensas.json        # lista persistente de ofensas
├── config.py           # constantes (nome do canal, prefixo)
└── requirements.txt    # discord.py
```

## Comportamento

### Tarefa agendada (a cada 4 horas)

1. Busca todos os membros do servidor
2. Filtra fora bots (incluindo o próprio bot)
3. Para cada membro humano, sorteia uma ofensa aleatória da lista
4. Envia uma mensagem por membro no canal `#comandos` no formato:

```
@[menção] você é um [ofensa]
```

### Comando `/add-ofensa`

- Disponível para qualquer membro do servidor
- Adiciona a ofensa ao `ofensas.json` permanentemente
- Responde com confirmação: `Ofensa "[palavra]" adicionada com sucesso!`

## Dados

### ofensas.json (lista padrão inicial)

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

## Configuração

| Variável | Valor |
|---|---|
| `DISCORD_TOKEN` | variável de ambiente (nunca no código) |
| Canal de destino | `#comandos` (fixo no código) |
| Intervalo | 4 horas |

## Hospedagem

- **Plataforma:** Railway (plano gratuito)
- **Deploy:** via repositório GitHub privado
- **Token:** configurado como variável de ambiente no Railway

## Stack

- Python 3.11+
- discord.py (com suporte a slash commands via `app_commands`)
- Sem banco de dados — armazenamento em `ofensas.json`