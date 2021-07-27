import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

import libraries.quotes as quotes
import libraries.helperFunctions as helperFunctions
import libraries.bonusapis as apis
import libraries.imgutils as imgutils
from libraries.cooldown import has_cooldown

import time, datetime
from datetime import date
from datetime import datetime
from helperFunctions import add_to_embed
import os, subprocess, re

from secret import cont

from bot import ts
def setup(bot):
    bot.add_cog(info_commands(bot))

class info_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @cog_ext.cog_slash(name='help', description='Give you help.')
    async def help(self, ctx: SlashContext):
        # seting up an embed
        embed = discord.Embed(description="Info on the bot and how to use it", colour=discord.Colour.green())

        embed.set_author(name='Help')
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/314578387031162882/e4b98a4a9ca3315ca699ffe5cba5b8f1.png?size=1024')
        embed.add_field(name='Commands will be found on the website.',value='[Link to website](https://saiv123.github.io/discord-bot/website/)', inline=False)
        embed.add_field(name='Please invite me to other Discords',value='[Invite bot to server](https://discord.com/api/oauth2/authorize?client_id=314578387031162882&permissions=8&scope=bot%20applications.commands)', inline=False)

        embed.set_footer(text='Help Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    
    @cog_ext.cog_slash(name='hi', description='Am I here? Are you here? Is anyone really here?')
    async def hi(self, ctx: SlashContext):
        embed = discord.Embed(title='Hello', description='Hello {0}!!!'.format(ctx.author.mention), colour=imgutils.randomSaturatedColor())
        embed.set_footer(text='Sanity check by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    
    @cog_ext.cog_slash(name='github', description='See the github!')
    async def github(self, ctx: SlashContext):
        embed = discord.Embed(title= "GitHub Website for Bot", description="This is where you can see how the bot works", url="https://github.com/saiv123/discord-bot")
        embed.set_footer(text='Github Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    
    @cog_ext.cog_slash(name='invite', description='Add me to your server!')
    async def invite(self, ctx: SlashContext):
        embed = discord.Embed(colour=discord.Colour.green())
        embed.set_author(name='Invite the Bot to another server')
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/314578387031162882/e4b98a4a9ca3315ca699ffe5cba5b8f1.png?size=1024')
        embed.add_field(name='Please invite me to other Discords',value='[Invite bot to server](https://discord.com/api/oauth2/authorize?client_id=314578387031162882&permissions=8&scope=bot%20applications.commands)', inline=False)
        embed.set_footer(text='Invite Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    
    @cog_ext.cog_slash(name='stats', description='What am I up to?')
    @has_cooldown(10)
    async def stats(self, ctx: SlashContext):
        #get the memory stats of the computer
        raw = subprocess.Popen(['free', '-h'], stdout = subprocess.PIPE)
        output = str(raw.communicate()).split('\\n')
        temp = output[1].split(" ")
        while '' in temp: temp.remove('')
        percent = convertInt(temp[2]) / convertInt(temp[1])
        memory = temp[2]+"/"+temp[1]+"-"+percent+"%"

        #get the cpu stats of the computer
        cpu_percent = getCPUStats()
        CPU = str(cpu_percent)+"%"
        # calculating time bot has been on
        tso = time.time()
        msg = time.strftime("%H Hours %M Minutes %S Seconds",time.gmtime(tso - ts))
        # seting up an embed
        embed = discord.Embed(colour=imgutils.randomSaturatedColor())
        # setting the clock image
        embed.set_thumbnail(url="https://hotemoji.com/images/dl/h/ten-o-clock-emoji-by-twitter.png")
        embed.add_field(name='I have been awake for:', value=msg, inline=True)
        embed.add_field(name='Memory:',value=memory,inline=True)
        embed.add_field(name='CPU:',value=CPU,inline=True)
        # embed.add_field(name='My core body temperature:',value=temp.replace("temp=", ""), inline=True)
        # embed.add_field(name="Quote cus I know you're bored:", value='"' +quote['quote'] + '"\n\t~' + quote['author'], inline=False)

        embed.set_footer(text='Status Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    
    @cog_ext.cog_slash(name='contact', description='Contact my father' )
    async def contact(self, ctx: SlashContext):
        msg = "Discord: Sai#3400\nDiscord server: <https://discord.gg/2zUTJ7j>\n"
        if(ctx.channel.id == 674120261691506688):  # channel specific to my discord server
            msg += cont
        embed = discord.Embed(title="Sai's contact info")
        embed.add_field(name=msg, value=":heart: take care!!", inline=False)
        id = ctx.author.id
        #TODO: send in embed
        await ctx.send(embed=embed, hidden=True)
    
    @cog_ext.cog_slash(name='ping', description="What's my speed?")
    async def ping(self, ctx: SlashContext):
        embed = add_to_embed('Ping','Latency: {0}ms'.format(round(self.bot.latency*1000, 1)))[0]
        embed.set_footer(text='Ping Measured by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    
    def convertInt(string):
        string = string.replace('G','*1073741824').replace('M','*1048576').replace('K','*1024')
        num = float(eval(string))
        return num
    
    def getCPUStats():
        raw = subprocess.Popen(['mpstat', '-u', '-o', 'JSON'], stdout = subprocess.PIPE)
        data = json.loads(raw.communicate()[0])
        user = data["sysstat"]["hosts"][0]["statistics"][0]["cpu-load"][0]["usr"]
        system = data["sysstat"]["hosts"][0]["statistics"][0]["cpu-load"][0]["sys"]
        return user+system