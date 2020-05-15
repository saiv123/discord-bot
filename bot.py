import sys
import os
import asyncio
import discord
import wolframalpha
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import time
import datetime
import json
import random

# external libraies
import quotes
import prawn

os.chdir("/home/pi/discord-bot")

# list is ordered in [leon,sai]
ownerId = [231957319737540608, 240636443829993473]

f = open("token.txt", 'r')
TOKEN = f.read()
f.close()
del f

client = wolframalpha.Client("XLQWQ2-A2HU3H9Y7V")

description = "Its a Sick use less bot"
bot = commands.Bot(command_prefix='$', description=description)
ts = time.time()

def randomColor():
    return ""

def isOwner(ctx):
    for i in ownerId:
        if(ctx.author.id == i):
            return True
    return False

def msgReturn(type):
    data = json.load(open("msg.json"))
    typeM = data[type]
    msgData = random.choice(typeM)
    del data, typeM
    return msgData


@bot.event
async def on_ready():
    print('loged in as')
    print(bot.user.name)
    print(bot.user.id)
    await bot.change_presence(activity=discord.Game(name='$help'))
    print('current time - ' + str(ts))
    print('-------')


@bot.event
async def on_message(message):
    nameNote = "dmLogs.txt"
    if(message.author.id == 371865866704257025):
        await message.delete()
        await bot.process_commands(message)
    elif message.guild is None and message.author != bot.user:
        other = await bot.fetch_user(message.author.id)
        with open(nameNote, 'a') as file:
            file.write(str(datetime.datetime.now()) + " " + other.name + " -- " + message.content + "\n")
        await bot.process_commands(message)
    else:
        await bot.process_commands(message)



@bot.command()
async def sendDM(ctx, id: int, *, msg: str):
    """dms person with id"""
    if(isOwner(ctx)):
        user = bot.get_user(id)
        channel = await user.create_dm()
        await channel.send(msg)
    else:
        await ctx.send("An error as occurred, please do not contact me about it.")


@bot.command()
async def status(ctx, type: str, *, other="https://twitch.tv/saiencevanadium/"):
    """sets the status for the bot"""
    if(isOwner(ctx)):
        if(type.lower() == "stream"):
            await bot.change_presence(activity=discord.Streaming(name="Watching my creator", url=other))
        elif(type.lower() == "help"):
            await bot.change_presence(activity=discord.Game(name='$help'))
        elif(type.lower() == "music"):
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=other))
        elif(type.lower() == "watching"):
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=other))
    else:
        await ctx.send(msgReturn("notOwner"))


@bot.command()
async def getnotes(ctx):
    """Dms you your last 5 notes"""
    try:
        notes = ""
        nameNote = ("MyPorn/" + str(ctx.author.id) + ".txt")
        f = open(nameNote, "r")
        temp = f.readlines()
        lineNums = len(temp)

        if(lineNums <= 5):
            for i in temp:
                notes += str(i)
        else:
            for i in range(lineNums - 5, lineNums):
                notes += str(temp[i])
        channel = await ctx.author.create_dm()
        await channel.send(notes)
    except IOError:
        print("File Not Found")
        channel = await ctx.author.create_dm()
        await channel.send("You do not have any notes")


@bot.command()
async def deletenotes(ctx):
    """Deletes ALL your notes"""
    nameNote = ('MyPorn/' + str(ctx.author.id) + '.txt')
    command = 'sudo rm -r ' + nameNote
    os.system(command)
    await ctx.send("Your Personal Notes have been Destroyed")


@bot.command()
async def notes(ctx, *, notes):
    """You can add notes to your notes file"""
    nameNote = ("MyPorn/" + str(ctx.author.id) + ".txt")
    await ctx.message.delete()
    user = ("<@" + str(ctx.message.author.id) + "> ")
    with open(nameNote, 'a') as file:
        file.write(str(datetime.datetime.now()) + " -- " + notes + "\n")
    await ctx.send(user + "Your Note is recorded and locked up.")
    del nameNote


@bot.command()
async def uptime(ctx):
    """Gives current up time"""
    tso = time.time()
    await ctx.send(time.strftime("%H:%M:%S", time.gmtime(tso - ts)))


@bot.command()
async def DefInte(ctx, a: int, b: int, func: str):
    """finds the intergral $DefInte a b f(x)"""
    res = client.query('integrate ' + func + ' from ' +
                       str(a) + ' to ' + str(b))
    await ctx.send(next(res.results).text)


@bot.command()
async def quote(ctx):
    """Give you heart warming quotes"""
    # await ctx.send(msgReturn("quotes")+" :heart:")
    await ctx.send(quotes.formatQuote(text=quotes.getQuoteJSON()[0] + " :heart:"))


@bot.command()
async def off(ctx):
    """This does ThInGs dont touch"""
    if(isOwner(ctx)):
        await ctx.send(msgReturn("offMsg"))
        await bot.logout()
        sys.exit(0)
    else:
        await ctx.send(msgReturn("notOwner"))


@bot.command()
async def nsfw(ctx, *args):
    """This command does what you think it does. NSFW"""
    if(ctx.guild is None and message.author != bot.user):
        await ctx.send("You Dumb stupid you are not allowed to use this command in dms")
    else:
        if(ctx.channel.is_nsfw()):
            query = ' '.join(args)
            if 'category' in query.lower() or 'categories' in query.lower():
                color = random.randrange(10000,16777215,1)
                for message in prawn.getCategoryMessages():
                    em = discord.Embed(description=message,color=color)
                    await ctx.send(embed = em)
            else:
                pu = ('Error','https://www.prajwaldesai.com/wp-content/uploads/2014/01/error-code.jpeg')
                if len(str(query)) <= 5:
                    pu = prawn.getRandom()
                else:
                    pu = prawn.getRandomLineFromQuery(query)
                print(pu)
                em = discord.Embed(description=pu[0],color=random.randrange(10000,16777215,1)) #16777... is just FFFFFF in base10
                em.set_image(url = pu[1])
                await ctx.send(embed = em)
        else:
            await ctx.send("Sorry, but this command can only be used in a NSFW channel.")

bot.run(TOKEN)
