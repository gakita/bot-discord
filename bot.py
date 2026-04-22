import io
import os
import random
import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv

from config import CANAL_NOME, INTERVALO_HORAS
from ofensas_manager import carregar_ofensas, adicionar_ofensa
from imagens_manager import carregar_imagem_aleatoria, salvar_imagem, listar_imagens
from ranking_manager import registrar_zoacao, carregar_ranking

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

PORCOS = ["🐷", "🐽", "🐖"]


async def zoar_membro(membro: discord.Member) -> tuple[str, discord.File | None]:
    ofensas = carregar_ofensas()
    ofensa = random.choice(ofensas)
    texto = f"{membro.mention} {ofensa}"
    registrar_zoacao(membro.id, membro.display_name)

    resultado = carregar_imagem_aleatoria()
    if resultado:
        dados, nome = resultado
        arquivo = discord.File(io.BytesIO(dados), filename=nome)
        return texto, arquivo

    return texto, None


@tasks.loop(hours=INTERVALO_HORAS)
async def zoar_membros():
    for guild in bot.guilds:
        canal = discord.utils.get(guild.text_channels, name=CANAL_NOME)
        if canal is None:
            continue
        membros = [m for m in guild.members if not m.bot]
        membro = random.choice(membros)
        texto, arquivo = await zoar_membro(membro)
        await canal.send(texto, file=arquivo)


@bot.event
async def on_ready():
    guild = discord.Object(id=int(os.environ["GUILD_ID"]))
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)
    if not zoar_membros.is_running():
        zoar_membros.start()
    print(f"Bot conectado como {bot.user}")


@bot.tree.command(name="zoar", description="Usa ai neguinho de merda")
async def zoar(interaction: discord.Interaction):
    membros = [m for m in interaction.guild.members if not m.bot]
    membro = random.choice(membros)
    texto, arquivo = await zoar_membro(membro)
    await interaction.response.send_message(texto, file=arquivo)


@bot.tree.command(name="zoar-alvo", description="Zoar alguém específico")
@app_commands.describe(alvo="O coitado que vai apanhar")
async def zoar_alvo(interaction: discord.Interaction, alvo: discord.Member):
    texto, arquivo = await zoar_membro(alvo)
    await interaction.response.send_message(texto, file=arquivo)


@bot.tree.command(name="ranking-zoados", description="Ranking dos mais zoados do servidor")
async def ranking_zoados(interaction: discord.Interaction):
    ranking = carregar_ranking()
    if not ranking:
        await interaction.response.send_message("Ninguém foi zoado ainda 🐷", ephemeral=True)
        return

    total = sum(r["count"] for r in ranking)
    medalhas = ["🥇", "🥈", "🥉"]
    linhas = []

    for i, entry in enumerate(ranking):
        medalha = medalhas[i] if i < 3 else f"{i+1}."
        porco = random.choice(PORCOS)
        linhas.append(f"{medalha} {entry['username']} — {entry['count']} zoações {porco}")

    lista = "\n".join(linhas)
    mensagem = f"🐷🐷🐷 **RANKING DOS ZOADOS** 🐷🐷🐷\n\n{lista}\n\n🐷 *Total de zoações no servidor: {total}* 🐷"
    await interaction.response.send_message(mensagem)


@bot.tree.command(name="listar-ofensas", description="Lista todas as ofensas do banco")
async def listar_ofensas(interaction: discord.Interaction):
    ofensas = carregar_ofensas()
    lista = "\n".join(f"{i+1}. {o}" for i, o in enumerate(ofensas))
    await interaction.response.send_message(f"**Ofensas cadastradas:**\n{lista}", ephemeral=True)


@bot.tree.command(name="add-ofensa", description="Adiciona uma nova negrice ao server")
@app_commands.describe(ofensa="A ofensa a ser adicionada")
async def add_ofensa(interaction: discord.Interaction, ofensa: str):
    adicionar_ofensa(ofensa)
    await interaction.response.send_message(f'Ofensa "{ofensa}" adicionada com sucesso! neeeeeeeeeeeeggaaaaaaaaaaaaa')


@bot.tree.command(name="mandar-imagem", description="Manda uma imagem pra alguém aleatório")
async def mandar_imagem(interaction: discord.Interaction):
    resultado = carregar_imagem_aleatoria()
    if not resultado:
        await interaction.response.send_message("Nenhuma imagem no banco.", ephemeral=True)
        return
    membros = [m for m in interaction.guild.members if not m.bot]
    membro = random.choice(membros)
    dados, nome = resultado
    arquivo = discord.File(io.BytesIO(dados), filename=nome)
    await interaction.response.send_message(membro.mention, file=arquivo)


@bot.tree.command(name="add-imagem", description="Adiciona uma imagem ao banco")
@app_commands.describe(imagem="A imagem a ser adicionada")
async def add_imagem(interaction: discord.Interaction, imagem: discord.Attachment):
    await interaction.response.defer(ephemeral=True)
    dados = await imagem.read()
    salvar_imagem(imagem.filename, dados)
    await interaction.followup.send(f'Imagem "{imagem.filename}" adicionada com sucesso!', ephemeral=True)


@bot.tree.command(name="listar-imagens", description="Lista todas as imagens do banco")
async def listar_imagens_cmd(interaction: discord.Interaction):
    imagens = listar_imagens()
    if not imagens:
        await interaction.response.send_message("Nenhuma imagem no banco.", ephemeral=True)
        return
    lista = "\n".join(f"{i+1}. {nome}" for i, nome in enumerate(imagens))
    await interaction.response.send_message(f"**Imagens cadastradas:**\n{lista}", ephemeral=True)


@bot.command(name="add-imagens")
async def add_imagens(ctx: commands.Context):
    if not ctx.message.attachments:
        await ctx.reply("Anexe pelo menos uma imagem junto com o comando.", mention_author=False)
        return
    salvos = []
    for anexo in ctx.message.attachments:
        if anexo.content_type and anexo.content_type.startswith("image/"):
            dados = await anexo.read()
            salvar_imagem(anexo.filename, dados)
            salvos.append(anexo.filename)
    if salvos:
        lista = "\n".join(f"✓ {n}" for n in salvos)
        await ctx.reply(f"{len(salvos)} imagem(ns) adicionada(s):\n{lista}", mention_author=False)
    else:
        await ctx.reply("Nenhuma imagem válida encontrada nos anexos.", mention_author=False)


if __name__ == "__main__":
    token = os.environ["DISCORD_TOKEN"]
    bot.run(token)
