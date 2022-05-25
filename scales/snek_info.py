import naff as dis

import libraries.imgutils as imgutils
from libraries.prawn import getClosestFromList

import json
import time
import holidays
from datetime import date, datetime
from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *

import subprocess
import json

from secret import cont
from snek_bot import ts

def memstrToNum(string):
    string = (
        string.replace("G", "*1073741824")
        .replace("M", "*1048576")
        .replace("K", "*1024")
    )
    num = float(eval(string))
    return num


def getCPUStats():
    raw = subprocess.Popen(["mpstat", "-u", "-o", "JSON"], stdout=subprocess.PIPE)
    data = json.loads(raw.communicate()[0])
    user = data["sysstat"]["hosts"][0]["statistics"][0]["cpu-load"][0]["usr"]
    system = data["sysstat"]["hosts"][0]["statistics"][0]["cpu-load"][0]["sys"]
    return float("{:.2f}".format(user + system))


class Info(dis.Extension):
    def __init__(self, bot: dis.Client):
        self.bot: dis.Client = bot
    
    @dis.slash_command(name="help", description="Get help on a command")
    async def help(self, ctx: dis.InteractionContext):
        # seting up an embed
        embed = dis.Embed(
            description="Info on the bot and how to use it",
            colour=dis.Colour.g,
        )

        embed.set_author(name="Help")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/314578387031162882/e4b98a4a9ca3315ca699ffe5cba5b8f1.png?size=1024"
        )
        embed.add_field(
            name="Commands will be found on the website.",
            value="[Link to website](https://saiv123.github.io/discord-bot/website/)",
            inline=False,
        )
        embed.add_field(
            name="Please invite me to other Discords",
            value="[Invite bot to server](https://discord.com/api/oauth2/authorize?client_id=314578387031162882&permissions=8&scope=bot%20applications.commands)",
            inline=False,
        )

        embed.set_footer(
            text="Help Requested by: " + ctx.author.display_name, icon_url=ctx.author.avatar.url
        )
        await ctx.send(embed=embed)

    @dis.slash_command(name="hi", description="Say hi to the bot")
    async def hi(self, ctx: dis.InteractionContext):
        embed = dis.Embed(
            title="Hello",
            description="Hello {0}!!!".format(ctx.author.mention),
            colour=imgutils.randomSaturatedColor(),
        )
        embed.set_footer(
            text="Sanity check by: " + ctx.author.display_name, icon_url=ctx.author.avatar.url
        )
        await ctx.send(embed=embed)
    
    @dis.slash_command(name="github", description="Get the link to the github repo")
    async def github(self, ctx: dis.InteractionContext):
        embed = dis.Embed(
            title="GitHub Website for Bot",
            description="This is where you can see how the bot works",
            url="https://github.com/saiv123/discord-bot",
        )
        embed.set_footer(
            text="Github Requested by: " + ctx.author.display_name,
            icon_url=ctx.author.avatar.url,
        )
        await ctx.send(embed=embed)
    
    @dis.slash_command(name="invite", description="Get the link to invite the bot to your server")
    async def invite(self, ctx: dis.InteractionContext):
        embed = dis.Embed(colour=dis.Color.g)
        embed.set_author(name="Invite the Bot to another server")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/314578387031162882/e4b98a4a9ca3315ca699ffe5cba5b8f1.png?size=1024"
        )
        embed.add_field(
            name="Please invite me to other Discords",
            value="[Invite bot to server](https://discord.com/api/oauth2/authorize?client_id=314578387031162882&permissions=8&scope=bot%20applications.commands)",
            inline=False,
        )
        embed.set_footer(
            text="Invite Requested by: " + ctx.author.display_name,
            icon_url=ctx.author.avatar.url,
        )
        await ctx.send(embed=embed)
    
    @dis.slash_command(name="stats", description="Get the bot's stats")
    async def stats(self, ctx: dis.InteractionContext):
        # Get the memory stats
        raw = subprocess.Popen(["free", "-h"], stdout=subprocess.PIPE)
        output = str(raw.communicate()).split("\\n")
        temp = [x for x in output[1].split(" ") if x != ""]
        percent = memstrToNum(temp[2]) / memstrToNum(temp[1])
        percent = "{:.2f}".format(percent * 100.0)
        memory = f"{temp[2]}/{temp[1]} - {percent}%"

        # Get CPU stats
        cpu_percent = f"{getCPUStats()}%"

        # calculating time bot has been on
        tso = time.time()
        msg = time.strftime("%H Hours %M Minutes %S Seconds", time.gmtime(tso - ts))

        # Set up and send embed
        embed = dis.Embed(title="Status", colour=imgutils.randomSaturatedColor())
        embed.set_thumbnail(
            url="https://hotemoji.com/images/dl/h/ten-o-clock-emoji-by-twitter.png"
        )  # set the clock image
        embed.add_field(name="I have been awake for:", value=msg, inline=False)
        embed.add_field(name="Memory:", value=memory, inline=True)
        embed.add_field(name="CPU:", value=cpu_percent, inline=True)
        embed.set_footer(
            text="Status Requested by: " + ctx.author.display_name,
            icon_url=ctx.author.avatar.url,
        )
        await ctx.send(embed=embed)
    
    @dis.slash_command(name="contact", description="Contact my father")
    async def contact(self, ctx: dis.InteractionContext):
        msg = "Discord: Sai#3400\nDiscord server: <http://discord.gg/dKWV3hS>\n"
        if (ctx.channel.id == 674120261691506688):  # channel specific to my discord server
            msg += cont

        embed = dis.Embed(title="Contact", colour=imgutils.randomSaturatedColor())
        embed.add_field(name="♥ Take Care", value=msg, inline=True)

        await ctx.send(embed=embed, hidden=True)
    
    @dis.slash_command(name="ping", description="Ping the bot")
    async def ping(self, ctx: dis.InteractionContext):
        embed = dis.Embed(title="Pong!", colour=imgutils.randomSaturatedColor())
        embed.add_field(name="Latency:", value=f"{ctx.bot.latency * 1000:.2f}ms", inline=True)
        embed.set_footer(
            text="Ping Measured by: " + ctx.author.display_name, icon_url=ctx.author.avatar.url
        )
        await ctx.send(embed=embed)

def setup(bot):
    Info(bot)