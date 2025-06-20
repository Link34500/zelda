import discord
from discord.ext import commands
import logging
import json
import constant

bot:commands.Bot = constant.BOT
datas:discord.TextChannel = constant.DATAS

async def load_serverfile(guild_id:int,file_name):
    
    # On vérifie si la guild existe
    logging.info(f"Guild search with ID {guild_id}")
    try:
        guild:discord.Guild = bot.fetch_guild(guild_id)
        logging.info(f"Guild found ! {guild.id}")
    except discord.NotFound:
        logging.info(f"Guild by ID : {guild_id} Not Found")
        return
    
    # Si la guild existe on récupère son data sous forme de dictionnaire
    guild_data = get_data_guild(guild_id)

    messages_links = get_files_id(guild_data,file_name)
    # Récupère les liens des message qui contienne le data dans le thread
    for link in messages_links:
        thread:discord.Thread = await datas.get_thread(guild_data['data_id'])
        message:discord.Message = thread.get_partial_message(link).fetch()
        message.add_files()
    datas.get_thread()

def get_files_id(guild_data,file_name):
    logging.debug(f"Les ID des fichiers de donnée du serveur {guild_data['id']} sont les suivants : {guild_data['files'].get(file_name)}")
    # Retourne la liste d'id des message qui contienne le fichier de donnée
    return guild_data['files'].get(file_name)

def get_data_guild(guild_id):
    with open("index.json",'r',enconding="utf-8") as f:
        index = json.load(f)
    for guild_data in index['guilds']:
        if guild_data['id'] == guild_id:
            return guild_data