import discord
import wolframalpha
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from bot import client

# external libraies
import libraries.quotes as quotes
import libraries.helperFunctions as helperFunctions
import libraries.bonusapis as apis
import libraries.imgutils as imgutils

class math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    definte_options = [
        {
            "name":"func",
            "description":"The function to integrate",
            "type":3,
            "required":True
        },
        {
            "name":"a",
            "description":"Integral lower bound",
            "type":3,
            "required":True
        },
        {
            "name":"b",
            "description":"Integral upper bound",
            "type":3,
            "required":True
        
        }
    ]

    wolfram_options = [
        {
            "name":"query",
            "description":"What should i ask?"
            "type":3
            "required":True
        }
    ]

    @cog_ext.cog_slash(name='definte', description='Calculate a definite integral.', options=definte_options, guild_ids=[648012188685959169])
    async def definte(self, ctx: SlashContext, a:int=0, b:int=0, func:str=''):
        # bunch of text formating to put into the api
        res = client.query('integrate ' + func + ' from ' +str(a) + ' to ' + str(b))
        # getting the answer from the api and parsing
        await ctx.send(next(res.results).text)
    
    @cog_ext.cog_slash(name='wolfram', description='Calculate anything!', options=wolfram_options, guild_ids=[648012188685959169])
    async def wolfram(self, ctx: SlashContext, query:str=''):
        res = client.query(query)
        res = list(res.results)

        embed=discord.Embed(title="Wolfram Aplha", description=query)
        embed.set_thumbnail(url="https://cdn.iconscout.com/icon/free/png-512/wolfram-alpha-2-569293.png")

        for i in range(len(res)):
            opener = True
            for msg in splitLongStrings(res[i].text, chars=1024):
                embed.add_field(name='Answer {}:'.format(i+1) if opener and len(res) > 1 else chr(0xffa0)*i+1,value=msg, inline=False)
                opener = False

        embed.set_footer(text='Answer Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(math(bot))