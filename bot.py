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

load_dotenv()

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


async def montar_mensagem(mention: str) -> tuple[str, discord.File | None]:
    ofensas = carregar_ofensas()
    ofensa = random.choice(ofensas)
    texto = f"{mention} {ofensa}"

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
        texto, arquivo = await montar_mensagem(membro.mention)
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
    texto, arquivo = await montar_mensagem(membro.mention)
    await interaction.response.send_message(texto, file=arquivo)


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


if __name__ == "__main__":
    token = os.environ["DISCORD_TOKEN"]
    bot.run(token)
