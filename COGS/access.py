import discord
from discord.utils import get
from discord.ext import commands, tasks
from asyncio import sleep
import json
import requests
from funcs import get_key_from_dc, holds_weeblet_dao, get_bulk_keys

config = json.load(open("config.json", "r"))

class Access(commands.Cog):
    def __init__(self, bot:discord.Bot):
        self.bot = bot
        self.dao_guild = bot.get_guild(config["GUILD"])
        if self.dao_guild is not None:
            self.welcome_channel = get(self.dao_guild.text_channels, id=config["WELCOME_CHANNEL"])
            self.dao_role  = self.dao_guild.get_role(config["DAO_ROLE"])
            self.waiting_role = self.dao_guild.get_role(config["WAITING_ROLE"])
        self.give_roles.start()
        
    @tasks.loop(minutes=2)
    async def give_roles(self):
        if self.dao_guild is not None:
            members = self.dao_guild.members
            m_ids = []
            for m in members:
                if not m.bot:
                    m_ids.append(m.id)
            # print(m_ids)
            idkeys = get_bulk_keys(m_ids)
            for id in idkeys:
                pubkey = idkeys[id]
                id = int(id)
                mem = get(members, id=id)
                try:
                    if holds_weeblet_dao(pubkey):
                        await mem.edit(roles=[self.dao_role])
                    else:
                        await mem.edit(roles=[self.waiting_role])    
                except Exception as e:
                    print("give_roles", e)
            
def setup(bot):
    bot.add_cog(Access(bot))
    print("LOADED COG: access.py")
