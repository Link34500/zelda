import aiohttp.connector
import discord
from discord.ext import commands
import logging
import json
import constant

bot:commands.Bot = constant.BOT
datas:discord.TextChannel = constant.DATAS

async def write_serverfile(guild_id:int,file_name,bytes:bytes):
    # 8Mo en octets
    part_size = 8 * 1024 * 1024
    data = []
    # Parcours le champ de bytes avec un pas de 8Mo
    for i in range(0,len(bytes),part_size):
        # Le mets dans une liste
        data.append(bytes[i:i+part_size])

    guild = get_data_guild(guild_id)
    guild["files"][file_name] = []
    thread:discord.Thread = await datas.get_thread(guild['data_id'])
    for part in data:
        message_part = await thread.send(file_name=file_name,file=discord.File(part))
        guild["files"][file_name].append(message_part.id)
    with open("index.json",'w',encoding="utf-8") as f:
        json.dump()


async def load_serverfile(guild_id:int,file_name):
    # On vérifie si la guild existe
    logging.info(f"Guild search with ID {guild_id}")
    try:
        guild:discord.Guild = await bot.fetch_guild(guild_id)
        logging.info(f"Guild found ! {guild.id}")
    except discord.NotFound:
        logging.info(f"Guild by ID : {guild_id} Not Found")
        return None
    
    # Si la guild existe on récupère son data sous forme de dictionnaire
    guild_data = get_data_guild(guild_id)

    messages_links = get_files_id(guild_data,file_name)
    # Récupère les liens des message qui contienne le data dans le thread
    data = bytearray()
    thread:discord.Thread = datas.get_thread(guild_data['data_id'])
    for link in messages_links:
        message:discord.Message = await thread.get_partial_message(link).fetch()
        data += message.attachments[0].read()
    return bytes(data)

def get_files_id(guild_data,file_name):
    logging.debug(f"Les ID des fichiers de donnée du serveur {guild_data['id']} sont les suivants : {guild_data['files'].get(file_name)}")
    # Retourne la liste d'id des message qui contienne le fichier de donnée
    return guild_data['files'].get(file_name)

def get_data_guild(guild_id):
    with open("index.json",'r',encoding="utf-8") as f:
        index = json.load(f)
    for guild_data in index['guilds']:
        if guild_data['id'] == guild_id:
            return guild_data
    return None