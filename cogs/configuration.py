import discord
from discord.ext import commands
from discord import app_commands
import utils.inputs as inputs
import logging
import json

import utils.inputs
# Les différentes options du menu de configuration ⚙️
with open('menu.json','r',encoding='utf-8') as file:
    menus = json.load(file)


class Menu(discord.ui.Select):
    def __init__(self,last_interaction:discord.Interaction,custom_id:str,author:bool=False,permissions:list=[]): 
        if menus.get(custom_id) is None:
            logging.error(f"The menu {custom_id} not found in menu.json")
            return
        self.last_interaction = last_interaction
        self.require_author = author
        self.requiere_permissions = permissions
        super().__init__(custom_id=custom_id, placeholder=menus[custom_id]["placeholder"], options=[discord.SelectOption(label=i["label"],value=i["value"],description=i["description"],emoji=i["emoji"]) for i in menus[custom_id]["options"]])

    async def callback(self,interaction:discord.Interaction):
        if self.require_author and self.last_interaction.user.id != interaction.user.id:
            raise app_commands.MissingPermissions
        command = interaction.data["values"][0]
        argument = interaction.data["values"][0].split("_")[1]
        if command.startswith("OPENMENU"):
            menu = self.open_menu(argument)
            view = discord.ui.View().add_item(menu)
            await interaction.response.edit_message(view=view)
        if command.startswith("ADDROLE"):
            interaction.user

    def open_menu(self,menu_id):
        return Menu(self.last_interaction,custom_id=menu_id)


class Configuration(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        match error:
            case isinstance(error,app_commands.MissingPermissions):
                embed = inputs.NOT_PERMITTED(interaction.guild_id,)
                await interaction.response.send_message(embed=embed,ephemeral=True)

    @app_commands.command(
        name="config",
        description="Commande de configuration du bot"
    )
    @app_commands.describe(categorie="Choisir la categorie")
    @app_commands.checks.has_permissions(administrator=True)
    async def config(self,interaction:discord.Interaction,categorie:str):
        # Crée le menu déroulant avec les options modération🚨...
        menu = Menu(interaction,"configuration",True)
        view = discord.ui.View().add_item(menu)
        await interaction.response.send_message(view=view)


    @app_commands.command(name="test")
    async def test(self,interaction:discord.Interaction):
        print(interaction.data)
    @app_commands.command(name="purge")
    async def purge(self,interaction:discord.Interaction):
        with open("index.json",'w') as f:
            json.dump({},f)

        for thread in interaction.channel.threads:
            await thread.delete()

async def setup(bot:commands.Bot):
    await bot.add_cog(Configuration(bot))
