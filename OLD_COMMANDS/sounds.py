import asyncio, discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord import FFmpegPCMAudio

import os
from os import path
import subprocess
import math

saiID = 240636443829993473
saiServ = 648012188685959169
aquatrust = [288861358555136000, saiID, 361275648033030144]
derptrust = [
    401181826145845249,
    181488013627490305,
    255930764154109952,
    118996359616397312,
    150485718534324224,
    saiID,
]

trustServ = [531614305733574666, saiServ]


async def playSound(ctx, path):
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


class files:
    def get(path: str):
        files = os.listdir(path)
        temp = ""
        for f in files:
            if ".mp3" in f:
                i = f.index(".")
                f = f[:i]
                temp += f + "\n"
        return temp

    def getTime(path: str):
        raw = subprocess.Popen(["soxi", "-D", path], stdout=subprocess.PIPE)
        output = str(raw.communicate()[0]).split("\\n")
        rawTime = output[0].split("'")
        rawTime = float(math.ceil(float(rawTime[1])))
        return rawTime + 1.0


class sounds(commands.Cog):
    play_options = [
        {
            "name": "sound",
            "description": "what sound you want to use. If you dont know the file name use /sound list",
            "type": 3,
            "required": True,
        }
    ]

    def __init__(self, bot):
        self.bot = bot

    # play command
    @cog_ext.cog_subcommand(
        base="sound",
        name="play",
        options=play_options,
        description="Plays sounds files",
        guild_ids=trustServ,
    )
    async def play(self, ctx: SlashContext, sound: str):
        fileName = sound + ".mp3"
        path = "error"
        for root, dirs, files in os.walk("./sounds/"):
            for name in files:
                if name == fileName:
                    path = os.path.join(root, name)
        try:
            if path == "error":
                await ctx.send("No such sound exists", hidden=True)
                return
            if ctx.author.id == saiID and ctx.guild.id == saiServ:
                await playSound(ctx, path)
            elif ctx.guild.id == saiServ:
                if ctx.author.id in aquatrust:
                    await playSound(ctx, path)
                elif ctx.author.id in derptrust:
                    await playSound(ctx, path)
                else:
                    await ctx.send("i solemnly swear i am up to no good")
                    raise NotTrusted("Don't worry about it")
            elif ctx.guild.id == 531614305733574666:
                if ctx.author.id in derptrust:
                    await playSound(ctx, path)
                else:
                    await ctx.send("i solemnly swear i am up to no good")
                    raise NotTrusted("Don't worry about it")
        except AttributeError as e:
            print(e)
            await ctx.send("your not in vc ;(", hidden=True)
        except NotTrusted as e:
            print(e)
            await ctx.send("OOF you dont have permitions to run this command.", hidden=True)

    # list command
    @cog_ext.cog_subcommand(
        base="sound", name="list", description="Lists sounds", guild_ids=trustServ
    )
    async def listAll(self, ctx: SlashContext):
        path = "./sounds/"
        if ctx.author.id == saiID and ctx.guild.id == saiServ:
            aquaTxt = files.get(path + "aqua/") + "\n"
            alexTxt = files.get(path + "alex/")
            await ctx.send(aquaTxt + alexTxt, hidden=True)
        elif ctx.guild.id == saiServ:
            if ctx.author.id in aquatrust:
                path = path + "aqua"
            elif ctx.author.id in derptrust:
                path = path + "alex"
            else:
                await ctx.send(
                    "OOF you dont have permitions to run this command.", hidden=True
                )
                return
        elif ctx.guild.id == 531614305733574666:
            if ctx.author.id not in derptrust:
                await ctx.send(
                    "OOF you dont have permitions to run this command.", hidden=True
                )
                return
            path = path + "alex"

        if path == "error":
            await ctx.send("ERROR Please put a file path!!", hidden=True)
        else:
            await ctx.send(files.get(path), hidden=True)