import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import time, datetime
from datetime import date
from datetime import datetime

# external libraies
import libraries.quotes as quotes
import libraries.helperFunctions as helperFunctions
import libraries.bonusapis as apis
import libraries.imgutils as imgutils


class stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name='stats', description='What am I up to?', guild_ids=[648012188685959169])
    async def stats(self, ctx: SlashContext):
        ts = time.time()
        quote = quotes.getQuoteApi()
        # temp = os.popen("vcgencmd measure_temp").readline()

        # calculating time bot has been on
        tso = time.time()
        msg = time.strftime("%H Hours %M Minutes %S Seconds",time.gmtime(tso - ts))
        # seting up an embed
        embed = discord.Embed(colour=imgutils.randomSaturatedColor())
        # setting the clock image
        embed.set_thumbnail(url="https://hotemoji.com/images/dl/h/ten-o-clock-emoji-by-twitter.png")
        embed.add_field(name='I have been awake for:', value=msg, inline=True)
        # embed.add_field(name='My core body temperature:',value=temp.replace("temp=", ""), inline=True)
        embed.add_field(name='Quote cus I know you\'re bored:', value='"' +quote['quote'] + '"\n\t~' + quote['author'], inline=False)

        embed.set_footer(text='Status Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(stats(bot))