import os
import random
import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv

from config import CANAL_NOME, INTERVALO_HORAS
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
        ofensas = carregar_ofensas()
        membros = [m for m in guild.members if not m.bot]
        for membro in membros:
            ofensa = random.choice(ofensas)
            await canal.send(f"{membro.mention} {ofensa}")


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
    ofensas = carregar_ofensas()
    membros = [m for m in interaction.guild.members if not m.bot]
    membro = random.choice(membros)
    ofensa = random.choice(ofensas)
    await interaction.response.send_message(f"{membro.mention} {ofensa}")


@bot.tree.command(name="add-ofensa", description="Adiciona uma nova negrice ao server")
@app_commands.describe(ofensa="A ofensa a ser adicionada")
async def add_ofensa(interaction: discord.Interaction, ofensa: str):
    adicionar_ofensa(ofensa)
    await interaction.response.send_message(f'Ofensa "{ofensa}" adicionada com sucesso! neeeeeeeeeeeeggaaaaaaaaaaaaa')


if __name__ == "__main__":
    token = os.environ["DISCORD_TOKEN"]
    bot.run(token)
