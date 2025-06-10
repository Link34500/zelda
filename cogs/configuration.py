import discord
from discord.ext import commands
from discord import app_commands

class Configuration(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @app_commands.command(
        name="config",
        description="Commande de configuration du bot"
    )
    @app_commands.default_permissions(perms="administrator")
    def config(self,interaction):
        pass