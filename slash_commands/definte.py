import discord
import wolframalpha
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from secrets import id


# external libraies
import libraries.quotes as quotes
import libraries.helperFunctions as helperFunctions
import libraries.bonusapis as apis
import libraries.imgutils as imgutils

class definte(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    client = wolframalpha.Client(id)
    definte_options = [
        {
            "name":"func",
            "description":"The function to integrate",
            "type":3,
            "required"=True
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

    @cog_ext.cog_slash(name='definte', description='Calculate a definite integral.', options=definte_options, guild_ids=[648012188685959169])
    async def definte(self, ctx: SlashContext,a:int=0, b:int=0, func:str=''):
        # bunch of text formating to put into the api
        res = client.query('integrate ' + func + ' from ' +str(a) + ' to ' + str(b))
        # getting the answer from the api and parsing
        await ctx.send(next(res.results).text)

def setup(bot):
    bot.add_cog(definte(bot))