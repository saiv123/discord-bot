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
    
    # command will change offten to test out commands
    @cog_ext.cog_slash(name='update', description='reloads all the cogs' )
    async def reload(self, ctx, *, cog: str="all"):
        if not isOwner(ctx):
        if cog == "all":
            cogs = []
            for cog in self.bot.cogs:
                cogs.append(cog)
        else: 
            cogs = [cog]
        response = reload_cogs(self.bot, cogs)
        await ctx.send(response, hidden=True)