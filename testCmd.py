import discord
from discord.ext import commands

class Members():
    def __init__(self, bot):
        self.bot = bot

    # command will change offten to test out commands
    @bot.command()
    async def test(ctx):
        await ctx.send("this is a test command :)")

def setup(bot):
    bot.add_cog(Members(bot))
