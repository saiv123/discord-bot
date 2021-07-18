import asyncio, discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord import FFmpegPCMAudio

import os

def setup(bot):
    bot.add_cog(sound_commands(bot))

class sound_commands(commands.Cog):
    aqua_options = [
        {
            "name": "sound",
            "description": "what sound you want to use. If you dont know the file name use /listsound",
            "type": 3,
            "required": True
        }
    ]
    def __init__(self, bot):
        self.bot = bot 
    
    class NotTrusted(Exception):
        pass

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
                raise NotTrusted('Dont worry about it')
        except AttributeError as e:
            print(e)
            await ctx.send("your not in vc ;(", hidden=True)
        except NotTrusted as e:
            print(e)
            await ctx.send("OOF you dont have permitions to run this command.", hidden=True)
    
    @cog_ext.cog_slash(name='listsound', description='List of sounds', guild_ids=[601247340887670792, 648012188685959169])
    async def listsound(self, ctx: SlashContext):
        trust = [288861358555136000, 240636443829993473, 361275648033030144]
        if ctx.author.id not in trust:
            await ctx.send("OOF you dont have permitions to run this command.", hidden=True)
            return
        path = './sounds'
        files = os.listdir(path)
        temp = ''
        for f in files:
            i = f.index('.')
            f = f[:i]
            temp += f+"\n"
        await ctx.send(temp, hidden=True)