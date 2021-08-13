import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

# external libraies
import libraries.quotes as quotes
import libraries.helperFunctions as helperFunctions
import libraries.bonusapis as apis
import libraries.imgutils as imgutils

import time, datetime
from datetime import date
from datetime import datetime

def setup(bot):
    bot.add_cog(quotes(bot))

class quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    
    @cog_ext.cog_slash(name='quote', description='Sends a heartwarming quote')
    async def quote(self, ctx: SlashContext):
        quote = apis.quote_to_discord_embed(quotes.getQuoteJSON())
        quote.set_thumbnail(url='https://clipart.info/images/ccovers/1531011033heart-emoji.png')
        quote.set_footer(text='Quote Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=quote)

    @cog_ext.cog_slash(name='randquote', description='Get a unique quote')
    async def randquote(self, ctx: SlashContext):
        quote = quotes.getQuoteApi()
        embed = apis.quote_to_discord_embed(quote)
        embed.set_footer(text='Quote Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    
    @cog_ext.cog_slash(name='advice', description='Sends a random piece of advice')
    async def advice(self, ctx: SlashContext):
        advice = apis.advice()
        embed = apis.quote_to_discord_embed(advice)
        embed.set_footer(text='Advice Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    
    @cog_ext.cog_slash(name='tronalddump', description='Sends 2 stupid trump quotes and attemps to gauge the difference')
    async def help(self, ctx: SlashContext):
        t = time.time()
        contra_tuple = apis.get_trump_contradiction()
        embeds = [apis.quote_to_discord_embed(i) for i in contra_tuple[1:]]

        nearest_contra_score = str(int(min(10,contra_tuple[0])))

        contra_meter = '0       1       2       3       4       5       6       7       8       9       10'.replace(nearest_contra_score, apis.number_to_discord_emote(nearest_contra_score))

        await ctx.send('For educational and mockery purposes only!')
        for embed in embeds:
            await ctx.send(embed=embed)
        await ctx.send('Contradiction Score:\n'+contra_meter+'\nScore: '+str(contra_tuple[0]))