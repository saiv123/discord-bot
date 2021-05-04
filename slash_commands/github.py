import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

# external libraies
import libraries.quotes as quotes
import libraries.helperFunctions as helperFunctions
import libraries.bonusapis as apis
import libraries.imgutils as imgutils


class github(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name='github', description='See the github!', guild_ids=[648012188685959169])
    async def github(self, ctx: SlashContext):
        embed = discord.Embed(title= "GitHub Website for Bot", description="This is where you can see how the bot works", url="https://github.com/saiv123/discord-bot")
        embed.set_footer(text='Github Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(github(bot))