import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

from secret import cont


class move(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    # Command to move user to where sai is in the Sai's server
    @cog_ext.cog_slash(name='move', description='Moves you to Sai', guild_ids=[648012188685959169])
    async def move(self, ctx: SlashContext):
        user = ctx.guild.get_member(240636443829993473)
        try:
            channel = ctx.author.voice.channel
            #also add logic for if sai is not in vc
            otherchannel = user.voice.channel
            #move logic
            await member.move_to(otherchannel, reason='Dont worry about it')
            await ctx.send("Boop Found him moving you to the vc Sai is in.", hidden=True)
        except AttributeError as e:
            #this is what it will do if user is not in vc
            await ctx.send("Sorry but you have to be in a vc to use this command\nOr Sai is not in a VC", hidden=True)

def setup(bot):
    bot.add_cog(move(bot))