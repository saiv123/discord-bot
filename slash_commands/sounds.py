import asyncio, discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord import FFmpegPCMAudio

import os
import subprocess
import math

saiID = 240636443829993473
saiServ = 648012188685959169
aquatrust = [288861358555136000, saiID, 361275648033030144]
derptrust = [401181826145845249, 181488013627490305, 255930764154109952, 118996359616397312, 150485718534324224, saiID]

trustServ = [601247340887670792, 531614305733574666, saiServ]

async def play(ctx, path):
    channel = ctx.author.voice.channel
    voice = await channel.connect()
    source = FFmpegPCMAudio(path)
    player = voice.play(source)
    time = files.getTime(path)
    await ctx.send("DONE", hidden=True)
    await asyncio.sleep(time)
    await ctx.guild.voice_client.disconnect()

class NotTrusted(Exception):
    pass

def setup(bot):
    bot.add_cog(sounds(bot))

class files():
    def get(path:str):
        files = os.listdir(path)
        temp = ''
        for f in files:
            i = f.index('.')
            f = f[:i]
            temp += f+"\n"
        return temp

    def getTime(path:str):
        raw = subprocess.Popen(['soxi', '-D', path], stdout = subprocess.PIPE)
        output = str(raw.communicate()[0]).split('\\n')
        rawTime = output[0].split('\'')
        rawTime = float(math.ceil(float(rawTime[1])))
        return rawTime+1.0

class sounds(commands.Cog):
    aqua_options = [
        {
            "name": "sound",
            "description": "what sound you want to use. If you dont know the file name use /aquasound",
            "type": 3,
            "required": True
        }
    ]

    alex_options = [
        {
            "name": "sound",
            "description": "what sound you want to use. If you dont know the file name use /alexsound",
            "type": 3,
            "required": True
        }
    ]

    list_options = [
        {
            "name": "file",
            "description": "For Sai only",
            "type": 3,
            "required": False
        }
    ]

    def __init__(self, bot):
        self.bot = bot 

    @cog_ext.cog_subcommand(base="sound", name='aqua', options=aqua_options, description='Makes baby noises', guild_ids=[601247340887670792, 648012188685959169])
    async def aqua(self, ctx: SlashContext, sound: str):
        path = './sounds/aqua/'+sound+'.mp3'
        try: 
            if ctx.author.id in aquatrust:
                await play(ctx, path)
            else:
                await ctx.send("i solemnly swear i am up to no good")
                raise NotTrusted('Don\'t worry about it')
        except AttributeError as e:
            print(e)
            await ctx.send("your not in vc ;(", hidden=True)
        except NotTrusted as e:
            print(e)
            await ctx.send("OOF you dont have permitions to run this command.", hidden=True)

    @cog_ext.cog_subcommand(base="sound", name='alex', options=alex_options, description='Makes sounds', guild_ids=[531614305733574666, 648012188685959169])
    async def alex(self, ctx: SlashContext, sound: str):
        path = './sounds/alex/'+sound+'.mp3'
        try:
            if ctx.author.id in derptrust:
                await play(ctx, path)
            else:
                await ctx.send("i solemnly swear i am up to no good")
                raise NotTrusted('Don\'t worry about it')
        except AttributeError as e:
            print(e)
            await ctx.send("your not in vc ;(", hidden=True)
        except NotTrusted as e:
            print(e)
            await ctx.send("OOF you dont have permitions to run this command.", hidden=True)
    
    @cog_ext.cog_subcommand(base="sound", name='list', options=list_options, description='Lists sounds', guild_ids=trustServ)
    async def list(self, ctx: SlashContext, folder:str="None"):
        folder = folder.lower()
        path = "./sounds/"
        if(ctx.author.id == saiID and ctx.guild.id == saiServ):
            if folder == "aqua":
                path=path+"aqua"
            elif folder == "alex":
                path=path+"alex"
            else:
                path = "ERROR"
        elif ctx.guild.id == saiServ:
            if ctx.author.id in aquatrust:
                path=path+"aqua"
            elif ctx.author.id in derptrust:
                path=path+"alex"
            else:
                await ctx.send("OOF you dont have permitions to run this command.", hidden=True)
                return
        elif ctx.guild.id == 601247340887670792:
            if ctx.author.id not in aquatrust:
                await ctx.send("OOF you dont have permitions to run this command.", hidden=True)
                return
            path=path+"aqua"
        elif ctx.guild.id == 531614305733574666:
            if ctx.author.id not in derptrust:
                await ctx.send("OOF you dont have permitions to run this command.", hidden=True)
                return
            path=path+"alex"
        
        if(path == "ERROR"):
            await ctx.send("ERROR Please put a file path!!", hidden=True)
        else:
            await ctx.send(files.get(path), hidden=True)

    #all list commands
    # @cog_ext.cog_subcommand(base="sound", name='aquaSounds', description='List of sounds', guild_ids=[601247340887670792, 648012188685959169])
    # async def aquasound(self, ctx: SlashContext):
    #     if ctx.author.id not in aquatrust:
    #         await ctx.send("OOF you dont have permitions to run this command.", hidden=True)
    #         return
    #     path = './sounds/aqua'
    #     await ctx.send(files.get(path), hidden=True)

    # @cog_ext.cog_subcommand(base="sound", name='alexSounds', description='List of sounds', guild_ids=[531614305733574666, 648012188685959169])
    # async def alexsound(self, ctx: SlashContext):
    #     if ctx.author.id not in derptrust:
    #         await ctx.send("OOF you dont have permitions to run this command.", hidden=True)
    #         return
    #     path = './sounds/alex'
    #     await ctx.send(files.get(path), hidden=True)