import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

# external libraies
import libraries.quotes as quotes
import libraries.helperFunctions as helperFunctions
import libraries.bonusapis as apis
import libraries.imgutils as imgutils


class quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    
    @cog_ext.cog_slash(name='quote', description='Sends a heartwarming quote', guild_ids=[648012188685959169])
    async def quote(self, ctx: SlashContext):
        quote = apis.quote_to_discord_embed(quotes.getQuoteJSON())
        quote.set_thumbnail(url='https://clipart.info/images/ccovers/1531011033heart-emoji.png')
        quote.set_footer(text='Quote Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=quote)

    @cog_ext.cog_slash(name='randquote', description='Get a unique quote', guild_ids=[648012188685959169])
    async def randquote(self, ctx: SlashContext):
        quote = quotes.getQuoteApi()
        embed = apis.quote_to_discord_embed(quote)
        embed.set_footer(text='Quote Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    
    @cog_ext.cog_slash(name='advice', description='Sends a random piece of advice', guild_ids=[648012188685959169])
    async def advice(self, ctx: SlashContext):
        advice = apis.advice()
        embed = apis.quote_to_discord_embed(advice)
        embed.set_footer(text='Advice Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(quotes(bot))