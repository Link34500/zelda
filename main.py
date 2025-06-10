import discord
from discord.ext import commands
import constant
import pathlib
import os

intents = discord.Intents.all()

bot = commands.Bot(intents=intents,command_prefix="!")

@bot.event
async def on_ready():
    print("Link... Link... Link... Wake Up !")
    constant.BOT = bot
    await load_cogs()
    await bot.tree.sync()
    print("Cogs Loads")

async def load_cogs():
    for filename in pathlib.Path(pathlib.Path("cogs")).iterdir():
        if filename.suffix == ".py" and filename != "__init__.py":
            await bot.load_extension(f"cogs.{filename.stem}")


bot.run(os.getenv("TOKEN"))