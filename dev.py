import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from libraries.helperFunctions import isOwner

import asyncio

def setup(bot):
    bot.add_cog(dev(bot))

class dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    reload_op = [
        {
            "name": "update",
            "description": "reloads all the cogs",
            "type": 3,
            "required": False
        }
    ]
    # command will change offten to test out commands
    @cog_ext.cog_slash(name='update', options=reload_op, description='reloads all the cogs' )
    async def reload(self, ctx, *, cog: str="all"):
        if not isOwner(ctx): return
        if cog == "all":
            cogs = []
            for cog in self.bot.cogs:
                cogs.append(cog)
        else: 
            cogs = [cog]
        response = self.bot.reload_extension(self.bot, cogs)
        await ctx.send(response, hidden=True)