import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext


class shouldI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    shouldI_options = [
        {
            "name":"msg",
            "description": "What I will record",
            "type": 3,
            "required": True
        }
    ]

    @cog_ext.cog_slash(name='shouldI', description='Ask my a should I question and i will tell you the answer.', options=shouldI_options, guild_ids=[648012188685959169])
    async def shouldI(self, ctx: SlashContext, msg: str):
        msg = " "+msg+" "
        # msg = ' '.join(msg)
        phrases = ['Yes! Go $','No, it won\'t work.','Hmmm, $ might be a fine idea','Unclear, consider rewording "/"','I don\'t know, ask someone else about $']
        embed = discord.Embed(title='Should I...', description='{}\n{}'.format(msg, random.choice(phrases).replace('/', msg)))
        embed.set_footer(text='Asked by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(shouldI(bot))