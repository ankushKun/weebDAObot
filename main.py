#!/usr/local/bin/python3.9

import json
import os
import discord
from decouple import config as env
from discord.ext import commands
import requests
from keep_alive import keep_alive

intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.voice_states = True

config = json.load(open("config.json", "r"))

bot = commands.Bot(command_prefix="-", self_bot=True, intents=intents)
def load_cogs():
    for file in os.listdir('./COGS'):
        if file.endswith('.py') and not file.startswith('_'):
            bot.load_extension(f'COGS.{file[:-3]}')


def unload_cogs():
    for file in os.listdir('./COGS'):
        if file.endswith('.py') and not file.startswith('_'):
            bot.unload_extension(f'COGS.{file[:-3]}')


@bot.event
async def on_ready():
    load_cogs()
    if bot.user is not None:
        print(f"--> {bot.user.name}#{bot.user.discriminator} online")
keep_alive()
bot.run(env("BOT_TOKEN"))
