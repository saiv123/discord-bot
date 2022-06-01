import naff as dis

from libraries.helperFunctions import isOwner

import asyncio
import os, sys
import time, datetime
from datetime import date
from datetime import datetime

trust = [648012188685959169, 272155212347736065]

class Dev(dis.Extension):
    def __init__(self, bot: dis.Client):
        self.bot = bot
    reload_op = dis.SlashCommandOption("update", dis.OptionTypes.STRING, "reloads all the cogs", False)
    
    @dis.subcommand(base="dev", name="update", description="reloads all the cogs", options=[reload_op])
    async def reload(self, ctx: dis.InteractionContext, cogType: str = "all"):
        if not isOwner(ctx):
            return  # not owner

        isHidden = not (ctx.guild.id in trust)  # checks for if to hide the message or not
        print(isHidden)  # sanity check

        # creating the embed color="#FFD700"
        embed = dis.Embed(
            title="Updating the bot...",
            color="#FFD700",
            timestamp=datetime.fromtimestamp(time.time()),)
        embed.set_footer(text="bot updated by: " + ctx.author.display_name, icon_url=ctx.author.avatar.url)

        # uses popen to run gin and its output
        stream = os.popen("git pull")
        output = stream.read()
        embed.add_field(name="Git Stats", value=output, inline=True)

        try:
            cogs = []

            if cogType == "all":
                for cog in self.bot.ext:
                    cogs.append(cog)
            else:
                cogs = [cogType]

            for cog in cogs:
                self.bot.reload_extension(cog)

            embed.add_field(
                name="Update Cogs", value="Done :white_check_mark:", inline=True
            )
            await ctx.send(embed=embed, ephemeral=isHidden)
        except:  # all other errors
            embed.add_field(name="Error", value=sys.exc_info()[0], inline=True)
            await ctx.send(embed=embed, ephemeral=isHidden)
            for i in sys.exc_info():
                print(i)
        
    @dis.subcommand(base="dev", name="load", description="reloads all the cogs", options=[reload_op])
    async def load(self, ctx: dis.InteractionContext, cogType: str = "all"):
        # checks if new .py files is in loaded cogs
        if not isOwner(ctx):
            return
        isHidden = not (ctx.guild.id in trust)
        embed = dis.Embed(
            title="Loading cogs",
            color="#FFD700",
            timestamp=datetime.fromtimestamp(time.time()),
        )
        embed.set_footer(
            text="loaded by: " + ctx.author.display_name, icon_url=ctx.author.avatar.url
        )

        try:
            notLoaded = []
            slashCommandsList = os.listdir("./slash_commands")
            if cogType.lower() == "all":
                for cog in self.bot.get_extensions():
                    pyCog = cog + ".py"
                    if pyCog not in slashCommandsList:
                        notLoaded.append("slash_commands." + cog)
            elif cogType + ".py" in slashCommandsList:
                notLoaded.append("slash_commands." + cog)
            else:
                embed.add_field(
                    name="ERROR", value=cogType + " not in files!!!!", inline=True
                )
                await ctx.send(embed=embed, ephemeral=isHidden)
                return

            if len(notLoaded) != 0:
                for unLoad in notLoaded:
                    self.bot.load_extension(unLoad)
            else:
                notLoaded.append("No Cogs to load All are loaded rn.")

            embed.add_field(name="Cogs loaded", value=notLoaded, inline=True)
            await ctx.send(embed=embed, ephemeral=isHidden)
        except:
            embed.add_field(name="Error", value=sys.exc_info()[0], inline=True)
            await ctx.send(embed=embed, ephemeral=isHidden)
            for i in sys.exc_info():
                print(i)

def setup(bot):
    Dev(bot)