import discord
from discord.ext import commands
import json

def message(name:str):
    return lambda placeholders=None: embed(name,placeholders=placeholders)
class Embed:
    NOT_PERMITTED = message("NOT_PERMITTED")

# Retourne l'embed avec les placeholders pour cherché par l'id
def embed(name,placeholders:dict=None):
    return