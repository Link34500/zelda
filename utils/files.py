import discord
from discord.ext import commands
import pathlib
import logging
import utils.functions
import json
import constant


async def append_guild(guild:discord.Guild):
    
    """Crée un espace de données pour le serveur indiqué si il n'existe pas

    Args:
        guild (discord.Guild): Serveur Discord objet entier
    """
    channel = utils.functions.get_channeldata()
    thread_name = [i.name for i in channel.threads]
    if not str(guild.id) in thread_name:
        with open("index.json",'r',encoding="utf-8") as f:
            index = json.load(f)
        data_thread:discord.Thread = await channel.create_thread(name=str(guild.id),type=discord.ChannelType.public_thread)
        logging.info(f"Thread de donnée créé pour le serveur avec ID {guild.id}")
        files = {}
        for filename in pathlib.Path("servers").iterdir():
            message = await data_thread.send(file=discord.File(pathlib.Path(filename),filename=filename.name))
            files[filename.name] = [message.id]
            logging.info(f"Le fichier {filename.name} à été chargée avec succès pour le serveur avec ID {guild.id}")
        index['guilds'].append({'name':guild.name,'id':guild.id,"data_id":data_thread.id,"premium":False,"files":files})
        with open("index.json",'w',encoding="utf-8") as f:
            json.dump(index,f,indent=4,ensure_ascii=True)


async def write_serverfile(guild_id:int,file_name,bytes):

    bot:commands.Bot = constant.BOT
    datas = utils.functions.get_channeldata()
    # 8Mo en octets
    part_size = 8 * 1024 * 1024
    data = []
    # Parcours le champ de bytes avec un pas de 8Mo
    for i in range(0,len(bytes),part_size):
        # Le mets dans une liste
        data.append(bytes[i:i+part_size])
    guild = get_data_guild(guild_id)

    
    print(datas.threads)
    for thread_for in datas.threads:
        if thread_for.id == guild['data_id']:
            thread:discord.Thread = thread_for
            # Supprime les anciens fichiers
            for files_for in guild["files"][file_name]:
                message = await thread.fetch_message(files_for)
                await message.delete()
                guild["files"][file_name].remove(files_for)
            for i,part in enumerate(data):
                import io
                
                message_part = await thread.send(file=discord.File(io.BytesIO(part),filename=f"{file_name}.part{i}"))
                guild["files"][file_name].append(message_part.id)
                logging.debug("Syncrohnisation local effecuter")
    logging.info("Envoie des données au serveur avec succès")
    with open("index.json",'r',encoding="utf-8") as f:
        index = json.load(f)
    for guild_for in index['guilds']:
        if guild_for['id'] == guild_id:
            index['guilds'].remove(get_data_guild(guild_id))
            index['guilds'].append(guild)
    with open("index.json",'w',encoding="utf-8") as f:
        json.dump(index,f,ensure_ascii=True,indent=4)


async def load_serverfile(guild_id:int,file_name:str):
    bot:commands.Bot = constant.BOT
    datas:discord.TextChannel = utils.functions.get_channeldata()

    # On vérifie si la guild existe
    logging.info(f"Guild search with ID {guild_id}")
    try:
        guild:discord.Guild = await bot.fetch_guild(guild_id)
        logging.info(f"Guild found ! {guild.id}")
    except discord.NotFound:
        logging.error(f"Guild by ID : {guild_id} Not Found")
        return None

    # Si la guild existe on récupère son data sous forme de dictionnaire
    guild_data = get_data_guild(guild_id)

    messages_links = get_files_id(guild_data,file_name)
    # Récupère les liens des message qui contienne le data dans le thread
    data = bytearray()

    for thread_for in datas.threads:
        if thread_for.name == str(guild_data['id']):
            thread:discord.Thread = thread_for

    for link in messages_links:
        message = await thread.fetch_message(link)
        message:discord.Message = await message.fetch()
        data += await message.attachments[0].read()
    
    return bytes(data)

def get_files_id(guild_data,file_name):
    if guild_data['files'].get(file_name) is None:
        logging.error(f"Le fichier de donnée nommé {file_name} n'as pas été trouvé")
    logging.debug(f"Les ID's du fichier {file_name} de donnée du serveur {guild_data['id']} sont les suivants : {guild_data['files'].get(file_name)}")
    # Retourne la liste d'id des message qui contienne le fichier de donnée
    return guild_data['files'].get(file_name)

def get_data_guild(guild_id):
    with open("index.json",'r',encoding="utf-8") as f:
        index = json.load(f)
    for guild_data in index['guilds']:
        if guild_data['id'] == guild_id:
            return guild_data
    return None