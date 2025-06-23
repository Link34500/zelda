import discord
from discord.ext import commands
import random
import json
import utils.functions
import utils.files

def text(name:str):
    return lambda interaction,embed=False, placeholders=None: message(interaction,name,placeholders,embed)

class Message:
    NOT_PERMITTED = text("NOT_PERMITTED")
    JOIN_MESSAGE = text("JOIN_MESSAGE")

async def message(interaction:discord.Interaction,name:str,placeholders:dict,embed):
    """Crée un message ou un embed

    Args:
        interaction: nécessésaire pour récupérer le contexte et les placeholders
        name: nom autodéfinie
        placeholders: dictionnaire optionnel pour remplacer du texte par défaut
        embed: bool pour savoir si il doit retourner un message ou un embed
    """

    placeholders.update(utils.functions.get_discord_placeholders())
    placeholders.update(utils.functions.get_placeholders())

    messages_json = await utils.files.load_serverfile(interaction.guild.id,'messages.json').decode(encoding='utf-8')
    
    # Récupère le message de réponse (aléatoire si plusieurs)
    response = random.choice(messages_json[name]["messages" if embed is False else "embeds"])
    # Remplace tout les placeholders de base
    for key,value in placeholders.items():
        if key in response:
            response.replace(key,value)
    
    if embed is False:
        return response
    
    embed = discord.Embed(
        title=response["title"],
        description=response["description"],
        color=discord.Colour(int(response["color"].replace('#',''),base=16))
    )
    
    for field in response["fields"]:
        embed.add_field(name=field["name"],value=field["value"],inline=field["inline"])
    
    embed.set_author()
    embed.set_footer()
    embed.set_thumbnail("")
    embed.set_image(response["image"])

    

    