import naff as dis

import libraries.quotesLib as quoteLib
import libraries.helperFunctions as helperFunctions
import libraries.bonusapis as apis
import libraries.imgutils as imgutils

import time, datetime
from datetime import date
from datetime import datetime

class Quotes(dis.Extension):
    def __init__(self, bot: dis.Client):
        self.bot: dis.Client = bot
    
    @dis.subcommand(base="quote", name="heartwarming", description="Sends a heartwarming quote")
    async def heartWarming(self, ctx: dis.InteractionContext):
        quote = apis.quote_to_discord_embed(quoteLib.getQuoteJSON())
        quote.set_thumbnail(
            url="https://clipart.info/images/ccovers/1531011033heart-emoji.png"
        )
        quote.set_footer(
            text="Quote Requested by: " + ctx.author.display_name,
            icon_url=ctx.author.avatar.url,
        )
        await ctx.send(embed=quote)

    @dis.subcommand(base="quote", name="randquote", description="Get a unique quote")
    async def randquote(self, ctx: dis.InteractionContext):
        quote = quoteLib.getQuoteApi()
        embed = apis.quote_to_discord_embed(quote)
        embed.set_footer(
            text="Quote Requested by: " + ctx.author.display_name,
            icon_url=ctx.author.avatar.url,
        )
        await ctx.send(embed=embed)

    @dis.subcommand(base="quote", name="advice", description="Sends a random piece of advice")
    async def advice(self, ctx: dis.InteractionContext):
        advice = apis.advice()
        embed = apis.quote_to_discord_embed(advice)
        embed.set_footer(
            text="Advice Requested by: " + ctx.author.display_name,
            icon_url=ctx.author.avatar.url,
        )
        await ctx.send(embed=embed)

def setup(bot):
    Quotes(bot)