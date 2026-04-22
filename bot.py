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
    guild = discord.Object(id=int(os.environ["GUILD_ID"]))
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)
    if not zoar_membros.is_running():
        zoar_membros.start()
    print(f"Bot conectado como {bot.user}")


@bot.tree.command(name="zoar", description="Dispara a zoação agora mesmo")
async def zoar(interaction: discord.Interaction):
    await interaction.response.send_message("Zoando...", ephemeral=True)
    await zoar_membros()


@bot.tree.command(name="add-ofensa", description="Adiciona uma nova ofensa à lista")
@app_commands.describe(ofensa="A ofensa a ser adicionada")
async def add_ofensa(interaction: discord.Interaction, ofensa: str):
    adicionar_ofensa(OFENSAS_FILE, ofensa)
    await interaction.response.send_message(f'Ofensa "{ofensa}" adicionada com sucesso!')


if __name__ == "__main__":
    token = os.environ["DISCORD_TOKEN"]
    bot.run(token)
