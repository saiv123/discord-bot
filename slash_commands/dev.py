import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from libraries.helperFunctions import isOwner

import asyncio
import os, sys
import time, datetime
from datetime import date
from datetime import datetime

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
    @cog_ext.cog_subcommand(base="dev", name='update', options=reload_op, description='reloads all the cogs' )
    async def reload(self, ctx, cogType: str="all"):
        trust = [648012188685959169, 272155212347736065]
        if not isOwner(ctx): return
        isHidden = not (ctx.guild.id in trust)
        print(isHidden)
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
                cogs = [cogType]
            
            for cog in cogs:
                self.bot.reload_extension("slash_commands."+cog)

            embed.add_field(name="Update Cogs", value="Done :white_check_mark:", inline=True)
            await ctx.send(embed=embed, hidden=isHidden)
        except discord.ext.commands.ExtensionNotLoaded as e:
            embed.add_field(name="Error", value=e, inline=True)
            await ctx.send(embed=embed, hidden=isHidden)
            print(e)
        except:
            embed.add_field(name="Error", value=sys.exc_info()[0], inline=True)
            await ctx.send(embed=embed, hidden=isHidden)
            for i in sys.exc_info():
                print(i)
    
    @cog_ext.cog_subcommand(base="dev", name='load', options=reload_op, description='loads new cogs' )
    async def load(self, ctx, cogType: str="all"):
        #checks if new .py files is in loaded cogs
        if not isOwner(ctx): return
        isHidden = not (ctx.guild.id in trust)
        embed = discord.Embed(title="Loading cogs", colour=discord.Color.gold(), timestamp= datetime.fromtimestamp(time.time()))
        embed.set_footer(text='loaded by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)

        try:
            notLoaded = []
            slashCommandsList = os.listdir('./slash_commands')
            if cogType.lower() == "all":
                for cog in self.bot.cogs:
                    pyCog = cog+".py"
                    if pyCog not in slashCommandsList:
                        notLoaded.append("slash_commands."+cog)
            elif cogType+".py" in slashCommandsList:
                notLoaded.append("slash_commands."+cog)
            else:
                embed.add_field(name="ERROR", value=cogType+" not in files!!!!", inline=True)
                await ctx.send(embed=embed, hidden=isHidden)
                return
            
            if len(notLoaded) != 0:
                for unLoad in notLoaded:
                    self.bot.load_extension(unLoad)
            else:
                notLoaded.append("No Cogs to load All are loaded rn.")

            embed.add_field(name="Cogs loaded", value=notLoaded, inline=True)
            await ctx.send(embed=embed, hidden=isHidden)
        except discord.ext.commands.ExtensionNotLoaded as e:
            embed.add_field(name="Error", value=e, inline=True)
            await ctx.send(embed=embed, hidden=isHidden)
            print(e)
        except:
            embed.add_field(name="Error", value=sys.exc_info()[0], inline=True)
            await ctx.send(embed=embed, hidden=isHidden)
            for i in sys.exc_info():
                print(i)