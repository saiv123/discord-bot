import os
import sys
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

import time, datetime
from datetime import date
from datetime import datetime

# external libraies
from libraries.helperFunctions import splitLongStrings


def setup(bot):
    bot.add_cog(notes(bot))


class notes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    make_notes_options = [
        {
            "name": "memory",
            "description": "What I will record",
            "type": 3,
            "required": True,
        }
    ]

    @cog_ext.cog_subcommand(
        base="notes",
        name="make",
        options=make_notes_options,
        description="Take a note!",
    )
    async def makeNotes(self, ctx: SlashContext, memory: str):
        nameNote = "MyPorn/" + str(ctx.author.id) + ".txt"

        # opens the file if the users file in there otherwise it will make it
        with open(nameNote, "a") as file:
            today = date.today()
            d1 = today.strftime("%d/%m/%Y")
            file.write(
                str(d1) + " -- " + memory + "\n"
            )  # formating and saving to the file
            embed = discord.Embed(title="Your Note is recorded and locked up.")
            embed.set_footer(
                text="Notes stored by: " + ctx.author.name,
                icon_url=ctx.author.avatar_url,
            )
            await ctx.send(
                embed=embed, hidden=True
            )  # hides the users message so others dont see what they saved

    @cog_ext.cog_subcommand(base="notes", name="get", description="Gets your notes")
    async def getNotes(self, ctx: SlashContext):
        # for the user to see their notes
        try:
            notes = ""
            nameNote = "MyPorn/" + str(ctx.author.id) + ".txt"
            f = open(nameNote, "r")
            temp = f.readlines()
            lineNums = len(temp)

            # will loop and get the last 5 notes saved
            if lineNums <= 5:
                for i in temp:
                    notes += str(i)
            else:
                for i in range(lineNums - 5, lineNums):
                    notes += str(temp[i])
            for message in splitLongStrings(notes):
                await ctx.author.send(message)
                await ctx.send("check your DM's.")
        except IOError:  # edge case if the user does not have any notes / file
            print("File Not Found")
            await ctx.author.send("You do not have any notes")

        embed = discord.Embed(title="Notes Retrieved")
        embed.set_footer(
            text="Notes used by: " + ctx.author.name, icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(
        base="notes", name="delete", description="Deletes your notes."
    )
    async def delNotes(self, ctx: SlashContext):
        # removes the personal files
        nameNote = "MyPorn/" + str(ctx.author.id) + ".txt"
        os.system(f"sudo rm -r {nameNote}")
        embed = discord.Embed(title="Notes destroyed")
        embed.set_footer(
            text="Notes destroyed by: " + ctx.author.name,
            icon_url=ctx.author.avatar_url,
        )
        await ctx.send(embed=embed)
