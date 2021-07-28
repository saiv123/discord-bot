import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from helperFunctions import add_to_embed

import libraries.imgutils as imgutils
from libraries.prawn import getClosestFromList
from libraries.cooldown import has_cooldown

import json
import time
import holidays
from datetime import date, datetime
from dateutil import parser

import subprocess
import json

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
    
    @cog_ext.cog_slash(
        name='daystill',
        description='Countdown towards the holidays',
        options=[
            create_option(
                name = "holiday",
                description =  "Which holiday?",
                option_type =  3,
                required =  False
            )
        ]
    )
    async def daystill(self, ctx:SlashContext, holiday:str=''):
        now = datetime.now()
        upcoming =  sorted( # Sort the list by most recent first
                        filter(
                            lambda x: now.date() < x[0] and (now.date().replace(year=now.year+1)) > x[0] and '(Observed)' not in x[1],   # If holiday is upcoming and within a year and not a shitty (Observed) marking
                            (BotHolidays(years=range(now.year-1, now.year+2))).items()                                                   # Check all holidays last year and next year
                        )
                    )

        # If no holidays given, give all upcoming ones
        if holiday.strip() == '': 
            upcoming_str = '\n'.join([f'{(x[0]-now.date()).days} days until {x[1]} ({x[0].strftime("%m/%d/%Y")})' for x in upcoming])
        
        # Else, if the holiday is a name, perform search
        elif not ('/' in holiday or '-' in holiday or ':' in holiday):
            closest_holiday = getClosestFromList([x[1] for x in upcoming], holiday)
            closest_holiday = [x for x in upcoming if x[1] == closest_holiday][0]
            upcoming_str = f'{(closest_holiday[0]-now.date()).days} days until {closest_holiday[1]} ({closest_holiday[0].strftime("%m/%d/%Y")})'
        
        # Else try to parse
        else:
            try:
                holiday_date = parser.parse(holiday)
                if holiday_date < now: holiday_date = holiday_date.replace(year=now.year+1)
                upcoming_str = f'{(holiday_date.date()-now.date()).days} days until {holiday}'
            except:
                upcoming_str = 'Error parsing date! Try again as month/day/year or search for a US holiday!'
        
        # Create and send embed
        embed = add_to_embed('Days Until', upcoming_str)
        embed.set_thumbnail(url='https://cdn.pixabay.com/photo/2017/06/10/06/39/calender-2389150_960_720.png')
        embed.set_footer(text='Day Awaited by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name='stats', description='What am I up to?')
    async def stats(self, ctx: SlashContext):
        # Get the memory stats
        raw = subprocess.Popen(['free', '-h'], stdout = subprocess.PIPE)
        output = str(raw.communicate()).split('\\n')
        temp = [x for x in output[1].split(" ") if x != '']
        percent = memstrToNum(temp[2]) / memstrToNum(temp[1])
        percent = float("{:.2f}".format(percent))
        memory = f'{temp[2]}/{temp[1]} - {percent}%'

        # Get CPU stats
        cpu_percent = f'{getCPUStats()}%'

        # calculating time bot has been on
        tso = time.time()
        msg = time.strftime("%H Hours %M Minutes %S Seconds",time.gmtime(tso - ts))
        
        # Set up and send embed
        embed = discord.Embed(title="Status",colour=imgutils.randomSaturatedColor())
        embed.set_thumbnail(url="https://hotemoji.com/images/dl/h/ten-o-clock-emoji-by-twitter.png") # set the clock image
        embed.add_field(name='I have been awake for:', value=msg, inline=False)
        embed.add_field(name='Memory:', value=memory, inline=True)
        embed.add_field(name='CPU:', value=cpu_percent, inline=True)
        embed.set_footer(text='Status Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    
    @cog_ext.cog_slash(name='contact', description='Contact my father' )
    async def contact(self, ctx: SlashContext):
        msg = "Discord: Sai#3400\nDiscord server: <http://discord.gg/dKWV3hS>\n"
        if(ctx.channel.id == 674120261691506688):  # channel specific to my discord server
            msg += cont
        
        embed = add_to_embed('♥ Take Care', msg)
        
        await ctx.send(embed=embed, hidden=True)
    
    @cog_ext.cog_slash(name='ping', description="What's my speed?")
    @has_cooldown(10)
    async def ping(self, ctx: SlashContext):
        embed = add_to_embed('Ping','Latency: {0}ms'.format(round(self.bot.latency*1000, 1)))[0]
        embed.set_footer(text='Ping Measured by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

class BotHolidays(holidays.UnitedStates):
    def _populate(self, year):
        holidays.UnitedStates._populate(self, year)

        if year >= 2000: self[date(year, 12, 7)] = 'My Father\'s Birthday'
        
        if year > 2020: self[date(year, 4, 12)] = f'My {year-2020}{self.st(year-2020)} Birthday'
        elif year == 2020: self[date(year, 4, 12)] = f'My Birthday'
        
        self[date(year, 4, 20)] = 'Dope Day'
        # TODO: add palindrome days

    def st(self, i:int):
        if i >= 20: i = int(str(int(i))[-1])
        if i == 1: return 'st'
        elif i == 2: return 'nd'
        elif i == 3: return 'rd'
        else: return 'th'

def memstrToNum(string):
    string = string.replace('G','*1073741824').replace('M','*1048576').replace('K','*1024')
    num = float(eval(string))
    return num

def getCPUStats():
    raw = subprocess.Popen(['mpstat', '-u', '-o', 'JSON'], stdout = subprocess.PIPE)
    data = json.loads(raw.communicate()[0])
    user = data["sysstat"]["hosts"][0]["statistics"][0]["cpu-load"][0]["usr"]
    system = data["sysstat"]["hosts"][0]["statistics"][0]["cpu-load"][0]["sys"]
    return user+system