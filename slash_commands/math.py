import discord
import wolframalpha

from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from libraries.helperFunctions import splitLongStrings
from bot import client

def setup(bot):
    bot.add_cog(math(bot))

class math(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name='definte',
        description ='Calculate a definite integral.',
        options=[
            create_option(
                name = "func",
                description =  "The function to integrate",
                option_type =  3,
                required =  True
            ),
            create_option(
                name =  "a",
                description =  "Integral lower bound",
                option_type =  3,
                required =  True
            ),
            create_option(
                name = "b",
                description = "Integral upper bound",
                option_type = 3,
                required = True
            )
        ]
    )
    async def definte(self, ctx= SlashContext, a:int=0, b:int=0, func:str=''):
        # bunch of text formating to put into the api
        res = client.query('integrate ' + func + ' from ' +str(a) + ' to ' + str(b))
        # getting the answer from the api and parsing
        await ctx.send(next(res.results).text)
    
    @cog_ext.cog_slash(
        name='wolfram',
        description='Calculate anything!',
        options=[
            create_option(
                name = "query",
                description = "What should i ask?",
                option_type = 3,
                required = True
            )
        ]
    )
    async def wolfram(self, ctx: SlashContext, query:str=''):
        res = client.query(query)
        res = list(res.results)

        embed=discord.Embed(title="Wolfram Aplha", description=query)
        embed.set_thumbnail(url="https://cdn.iconscout.com/icon/free/png-512/wolfram-alpha-2-569293.png")

        for i in range(len(res)):
            opener = True
            for msg in splitLongStrings(res[i].text, chars=1024):
                name = f'Answer {i+1}:' if opener and len(res) > 1 else str(chr(0xffa0)*(i+1))
                embed.add_field(name=str(name), value=str(msg), inline=False)
                opener = False

        embed.set_footer(text=f'Answer Requested by: {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)