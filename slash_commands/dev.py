import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from libraries.helperFunctions import isOwner

import asyncio
import os

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
    # updates the scripts
    @cog_ext.cog_slash(name='update', options=reload_op, description='reloads all the cogs' )
    async def reload(self, ctx, *, cogType: str="all"):
        if not isOwner(ctx): return
        embed = discord.Embed(title="Updating the bot...", colour=discord.Color.gold(), timestamp= datetime.fromtimestamp(time.time()))
        embed.set_footer(text='bot updated by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)

        stream = os.popen('git pull')
        output = stream.read()
        embed.add_field(name="Git Stats", value=output, inline=True)
        try:
            cogs = []
        
            if cogType == "all":
                for cog in self.bot.cogs:
                    cogs.append(cog)
            else: 
                cogs = [cog]
            
            for cog in cogs:
                self.bot.reload_extension("slash_commands."+cog)

            embed.add_field(name="Update Cogs", value="Done :white_check_mark:", inline=True)
            await ctx.send(embed=embed, hidden=True)
        except discord.ext.commands.ExtensionNotLoaded as e:
            embed.add_field(name="Error", value=e, inline=True)
            await ctx.send(embed=embed, hidden=True)
            print(e)