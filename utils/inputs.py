import random
import datetime
import utils.files
import discord


class _Inputs:
    def __init__(self):
        pass

    def text(self,name:str):
        async def function(guild_id,**kwargs):
            await self.message(guild_id,name,**kwargs)
        return function
    
    async def message(guild_id,name:str,**kwargs):
        messages_json = await utils.files.load_serverfile(guild_id,'messages.json')
        # Récupère le message de réponse (aléatoire si plusieurs)
        response:str = random.choice(messages_json["categories"][name])
        # Regarde si l'utilisateur à choisi une réponse en embeds ou en messages
        if messages_json[name]["embed"] is False:
            return response.format(**kwargs)
        message = messages_json[name]["embeds"]
        embed = discord.Embed(
            title= message["title"].format(**kwargs),
            description=response.format(**kwargs),
            color=int(message["color"].removeprefix('#'),16),
            timestamp=datetime.datetime.now() if message["time"] is True else None
        )
        if message["author"]["name"] != "":
            embed.set_author(message["author"]["name"].format(**kwargs),message["author"]["url"].format(**kwargs),message["author"]["icon_url"].format(**kwargs))

        if message["footer"]["text"] != "":
            embed.set_footer(text=message["footer"]["text"],icon_url=message["footer"]["icon_url"])

        for field in message["fields"]:
            if embed["fields"][field]["name"] != "":    
                embed.add_field(name=embed["fields"][field]["name"],inline=embed["fields"][field]["inline"],value=embed["fields"][field]["value"])
        
        return embed



NOT_PERMITTED = _Inputs().text("NOT_PERMITTED")
JOIN_MESSAGE = _Inputs().text("JOIN_MESSAGE")



