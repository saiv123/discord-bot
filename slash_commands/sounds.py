import asyncio, discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord import FFmpegPCMAudio

def setup(bot):
    bot.add_cog(sound_commands(bot))

class sound_commands(commands.Cog):
    aqua_options = [
        {
            "name": "sound",
            "description": "what sound you want to use. if you dont know the file name use /list",
            "type": 3,
            "required": True
        }
    ]
    def __init__(self, bot):
        self.bot = bot 
    
    @cog_ext.cog_slash(name='aqua', options=aqua_options, description='Makes baby noises', guild_ids=[601247340887670792, 648012188685959169])
    async def aqua(self, ctx: SlashContext, sound: str):
        path = './sounds/'+sound+'.mp3'
        try:
            trust = [288861358555136000, 240636443829993473, 361275648033030144]
            if ctx.author.id in trust:
                channel = ctx.author.voice.channel
                voice = await channel.connect()
                source = FFmpegPCMAudio(path)
                player = voice.play(source)
                await ctx.send("DONE", hidden=True)
                await asyncio.sleep(10)
                await ctx.guild.voice_client.disconnect()
            else:
                await ctx.send("i solemnly swear i am up to no good")
                raise AttributeError('Dont worry about it')
        except AttributeError as e:
            print(e)
            await ctx.send("OOF you cant run this command or your not in vc ;(", hidden=True)