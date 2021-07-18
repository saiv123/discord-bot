import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord import FFmpegPCMAudio

def setup(bot):
    bot.add_cog(sound_commands(bot))

class sound_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    
    @cog_ext.cog_slash(name='aqua', description='Makes baby noises', guild_ids=[601247340887670792, 648012188685959169])
    async def aqua(self, ctx: SlashContext):
        try:
            channel = ctx.author.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio('./sounds/good_child.mp3')
            player = voice.play(source)
            await ctx.send("DONE", hidden=True)
            print(voice.is_playing())
            while(voice.is_playing() == False):
                ctx.guild.voice_client.cleanup()
                await ctx.guild.voice_client.disconnect()
        except AttributeError as e:
            await ctx.send("OOF you cant run this command or your not in vc ;(", hidden=True)