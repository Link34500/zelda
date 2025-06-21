import discord
from discord.ext import commands
import constant
import logging
import utils.files
import pathlib
import os

intents = discord.Intents.all()

bot = commands.Bot(intents=intents,command_prefix="!")

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')

@bot.event
async def on_ready():
    logging.info("Link... Link... Link... Wake Up !")
    constant.BOT = bot
    await load_cogs()
    await bot.tree.sync()
    logging.info("Cogs Loads")
    # Crée les serveurs de données pour les guilds qui n'en n'ont pas
    for guild in bot.guilds:
        await utils.files.append_guild(guild)  # La fonction vérifie déjà si la guild contient un data

async def load_cogs():
    for filename in pathlib.Path("cogs").iterdir():
        if filename.suffix == ".py" and filename.name != "__init__.py":
            await bot.load_extension(f"cogs.{filename.stem}")


bot.run(os.getenv("TOKEN"))