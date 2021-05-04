import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

# external libraies
import libraries.quotes as quotes
import libraries.helperFunctions as helperFunctions
import libraries.bonusapis as apis
import libraries.imgutils as imgutils


class invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name='invite', description='Add me to your server!', guild_ids=[648012188685959169])
    async def invite(self, ctx: SlashContext):
        embed = discord.Embed(colour=discord.Colour.green())
        embed.set_author(name='Invite the Bot to another server')
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/314578387031162882/e4b98a4a9ca3315ca699ffe5cba5b8f1.png?size=1024')
        embed.add_field(name='Please invite me to other Discords',value='[Invite bot to server](https://discord.com/api/oauth2/authorize?client_id=314578387031162882&permissions=8&scope=bot)', inline=False)
        embed.set_footer(text='Invite Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(invite(bot))