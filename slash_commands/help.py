import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

# external libraies
import libraries.quotes as quotes
import libraries.helperFunctions as helperFunctions
import libraries.bonusapis as apis
import libraries.imgutils as imgutils


class helpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name='help', description='Give you help.', guild_ids=[648012188685959169])
    async def help(self, ctx: SlashContext):
        # seting up an embed
        embed = discord.Embed(description="Info on the bot and how to use it", colour=discord.Colour.green())

        embed.set_author(name='Help')
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/314578387031162882/e4b98a4a9ca3315ca699ffe5cba5b8f1.png?size=1024')
        embed.add_field(name='Commands will be found on the website.',value='[Link to website](https://saiv123.github.io/discord-bot/website/)', inline=False)
        embed.add_field(name='Please invite me to other Discords',value='[Invite bot to server](https://discord.com/api/oauth2/authorize?client_id=314578387031162882&permissions=8&scope=bot%20applications.commands)', inline=False)

        embed.set_footer(text='Help Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    
    @cog_ext.cog_slash(name='hi', description='Am I here? Are you here? Is anyone really here?', guild_ids=[648012188685959169])
    async def hi(self, ctx: SlashContext):
        embed = discord.Embed(title='Hello', description='Hello {0}!!!'.format(ctx.author.mention))
        embed.set_footer(text='Sanity check by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(helpCommand(bot))