import discord
from discord.utils import get
from discord.ext import commands, tasks
import json
import requests
from funcs import get_key_from_dc, holds_weeblet_dao

config = json.load(open("config.json", "r"))

class Welcome(commands.Cog):
    def __init__(self, bot:discord.Bot):
        self.bot = bot
        self.dao_guild = bot.get_guild(config["GUILD"])
        if self.dao_guild is not None:
            self.welcome_channel = get(self.dao_guild.text_channels, id=config["WELCOME_CHANNEL"])
            self.dao_role  = self.dao_guild.get_role(config["DAO_ROLE"])
            self.waiting_role = self.dao_guild.get_role(config["WAITING_ROLE"])

    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        print(f"{member} has joined the server!")
        desc = f"{member.mention} has joined the server!\nMake sure you have read <#979909106221609010> for important info."
        if self.welcome_channel is not None:
            user_id = member.id
            key = get_key_from_dc(user_id)
            if key is not None:
                if(holds_weeblet_dao(key)):
                    print("User is holding the weeblet dao")
                    if self.dao_guild is not None:
                        await member.edit(roles=[self.dao_role])
                        desc += "\n\nLooks like you are a member of the weebletDAO, access given"
                        emb = discord.Embed(title="Welcome to the weeblet DAO!",description=desc, color=0x00aaaa)
                        await self.welcome_channel.send(f"{member.mention}", embed=emb)
                else:
                    desc += "\n\nLooks like you dont hold any weebletDAO, can't give access\n(If this was a mistake, please contact weeblet)"
                    emb = discord.Embed(title="Welcome to the weeblet DAO!",description=desc, color=0x00aaaa)
                    await self.welcome_channel.send(f"{member.mention}", embed=emb)
                    await member.edit(roles=[self.waiting_role])
            else:
                desc += "Looks like your discord account is not connected to deso, head over to https://cordify.app/verify to do so ^_^"
                emb = discord.Embed(title="Welcome to the weeblet DAO!",description=desc, color=0x00aaaa)
                await self.welcome_channel.send(f"{member.mention}", embed=emb)
                await member.edit(roles=[self.waiting_role])

def setup(bot):
    bot.add_cog(Welcome(bot))
    print("LOADED COG: welcome.py")
