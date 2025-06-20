import discord
from discord.ext import commands
import constant
import logging
import json
import pathlib
import os

intents = discord.Intents.all()

bot = commands.Bot(intents=intents,command_prefix="!")

@bot.event
async def on_ready():
    with open("index.json",'r',enconding="utf-8"):
        index = json.load(f)
    logging.info("Link... Link... Link... Wake Up !")
    constant.BOT = bot
    await load_cogs()
    await bot.tree.sync()
    logging.info("Cogs Loads")
    # Chargemment du serveur de donnés
    logging.info("Recherche du serveur de donnés")
    try:
        serv_data:discord.Guild = bot.fetch_guild(1352303484183249061)
        logging.info("Serveur de donnés trouvé")
    except discord.NotFound:
        logging.critical("La communication avec le serveur de donnés à échouée")
        exit()
    for channel in serv_data.channels:
        if channel.name == bot.user.id:
            logging.info("Connexion avec le serveur de données établi avec succès")
            constant.DATAS = channel
            for guild in bot.guilds:
                thread_name = [i.name for i in channel.threads]
                # Si le serveur n'es pas lié au serveur de donnée il crée une liason grâce à un thread
                if not str(guild.id) in thread_name:
                    data_thread:discord.Thread = channel.create_thread(name=str(guild.id))
                    logging.info(f"Thread de donnée créé pour le serveur avec ID {guild.id}")
                    index['guilds'].append({'name':guild.name,'id':guild.id,"data_id":data_thread.id,"files":[]})
                    with open("index.json",'w',encoding="utf-8") as f:
                        json.dump(index,f,indent=4,ensure_ascii=True)
                logging.debug(f"Donnée de la guild {guild.id} établie")
            return
    logging.critical(f"Nous ne sommes pas parvenu à établir une connexion avec le serveur de donnés du bot avec ID {bot.user.id}")
    exit()


async def load_cogs():
    for filename in pathlib.Path("cogs").iterdir():
        if filename.suffix == ".py" and filename.name != "__init__.py":
            await bot.load_extension(f"cogs.{filename.stem}")


bot.run(os.getenv("TOKEN"))