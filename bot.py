#all of the py libraires used
import sys, os
import asyncio, discord
import wolframalpha
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import time, datetime
import json, random

# external libraies
import quotes, prawn

#dir for the bots location
os.chdir("/home/pi/discord-bot")

# List of Owners/Bot admins
ownerId = [231957319737540608, 240636443829993473]

#gets the bots personal token to boot
f = open("token.txt", 'r')
TOKEN = f.read()
f.close()
del f

#for the math stuff
client = wolframalpha.Client("XLQWQ2-A2HU3H9Y7V")

#setting up the bot, with its discritpion etc.
bot = commands.Bot(command_prefix='$', description="Its a Sick use-less bot")
ts = time.time()

# deleting default help comand
bot.remove_command('help')

""""""""""""""""""""""""""
"""bots helper commands"""
""""""""""""""""""""""""""

#used as a check for some command so only the people that are allowed to use it can use it
def isOwner(ctx):
    for i in ownerId:
        if(ctx.author.id == i):
            return True
    return False

#gets a message from the dictionary with the type inputed
def msgReturn(type):
    data = json.load(open("msg.json"))
    typeM = data[type]
    msgData = random.choice(typeM)
    del data, typeM
    return msgData

""""""""""""""""""""""""""""""""""""""
"""Inizalization of bot DO NOT EDIT"""
""""""""""""""""""""""""""""""""""""""

#starting the bot
@bot.event
async def on_ready():
    print('loged in as')
    print(bot.user.name)
    print(bot.user.id)
    await bot.change_presence(activity=discord.Game(name='with his food | $help'))
    print('current time - ' + str(ts))
    guilds = await bot.fetch_guilds(limit=150).flatten()
    print(str(len(guilds))+"\n")
    for i in guilds:
        print(i.name+" ")
    print('-------')

#for every message it does these checks
@bot.event
async def on_message(message):
    nameNote = "dmLogs.txt"
    if(message.author.id == 371865866704257025): #for removing bobcat from servers
        await message.delete()
        return
    elif message.guild is None and message.author != bot.user: #checks if theres a dm to the bot, and logs it
        other = await bot.fetch_user(message.author.id)
        with open(nameNote, 'a') as file:
            file.write(str(datetime.datetime.now()) + " " +
                       other.name + " -- " + message.content + "\n")
    
    # Respond to commands last
    await bot.process_commands(message)

""""""""""""""
"""Commands"""
""""""""""""""

#our curtom help command
@bot.command(pass_context=True)
async def help(ctx):
    #creats a channel object to dm the user the help command
    author = ctx.message.author
    channel = await author.create_dm()

    #seting up an embed
    embed = discord.Embed(
        colour=discord.Colour.green()
    )

    embed.set_author(name='Help')
    embed.add_field(name='$notes', value='You can add notes to your notes file', inline=False)
    embed.add_field(name='$deletenotes',value='Deletes ALL your notes', inline=False)
    embed.add_field(name='$getnotes',value='Dms you your last 5 notes', inline=False)
    embed.add_field(name='$uptime', value='The time the bot has been up in HH:MM:SS', inline=False)
    embed.add_field(name='$DefInte', value='Finds the intergral $DefInte a b f(x)', inline=False)
    embed.add_field(name='$quote', value='Give you heart warming quotes', inline=False)
    embed.add_field(name='$randquote', value='Give you a random quote', inline=False)
    embed.add_field(name='$nsfw', value='will give you a random nsfw image\nyou can choose a category from $nsfw category\nfrom the list you have to spell out the category excatly how it is sent to you as\n$nsfw [category]', inline=False)
    embed.add_field(name='$hi', value='Will send hi back to you', inline=False)
    embed.add_field(name='$contact', value='Will give you information on how to conact owner for support', inline=False)

    await channel.send(embed=embed)

#says hello to your
@bot.command()
async def hi(ctx):
    await ctx.message.delete()
    user = ("<@" + str(ctx.message.author.id) + "> ")
    await ctx.send("Hello "+user+"!!!!!!!")


#for the user to see their notes
@bot.command()
async def getnotes(ctx):
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

#removes the personal files
@bot.command()
async def deletenotes(ctx):
    nameNote = ('MyPorn/' + str(ctx.author.id) + '.txt')
    command = 'sudo rm -r ' + nameNote
    os.system(command)
    await ctx.send("Your Personal Notes have been Destroyed")

#logic for saving their notes
@bot.command()
async def notes(ctx, *, notes=" "):
    nameNote = ("MyPorn/" + str(ctx.author.id) + ".txt")
    await ctx.message.delete()
    user = ("<@" + str(ctx.message.author.id) + "> ")
    with open(nameNote, 'a') as file:
        file.write(str(datetime.datetime.now()) + " -- " + notes + "\n")
    await ctx.send(user + "Your Note is recorded and locked up.")
    del nameNote

#return the time the bot has been running
@bot.command()
async def uptime(ctx):
    tso = time.time()
    await ctx.send(time.strftime("%H:%M:%S", time.gmtime(tso - ts)))

#return the answers to deffenet integrals
@bot.command()
async def DefInte(ctx, a: int, b: int, func: str):
    res = client.query('integrate ' + func + ' from ' +
                       str(a) + ' to ' + str(b))
    await ctx.send(next(res.results).text)

#sends a warming quote
@bot.command()
async def quote(ctx):
    await ctx.send(quotes.formatQuote(text=quotes.getQuoteJSON()[0] + " :heart:"))

#sends a random quote
@bot.command()
async def randquote(ctx):
    async with ctx.channel.typing():
        quote, author = quotes.getQuoteApi()
        await ctx.send(quotes.formatQuote(text=quote,author=author))

# For getting memes from the library
memePath = 'ClassWork/'
@bot.command()
async def meme(ctx, *args):
    query = ' '.join(args)
    #logic for getting the category list
    if 'category' in query.lower() or 'categories' in query.lower():
        color = random.randrange(10000, 16777215, 1)
        for message in prawn.getCategoryMessages(path=memePath):
            em = discord.Embed(description=message, color=color)
            await ctx.send(embed=em)
    else: #Try and get category. If not possible, get a random meme
        pu = ('Error', 'https://www.prajwaldesai.com/wp-content/uploads/2014/01/error-code.jpeg')
        if len(str(query)) <= 2:
            pu = prawn.getRandom(path=memePath)
        else:
            pu = prawn.getRandomLineFromQuery(query,path=memePath)
        print(pu)
        em = discord.Embed(description=pu[0], color=random.randrange(10000, 16777215, 1))  # 16777... is just FFFFFF in base10
        em.set_image(url=pu[1])

        await ctx.send(embed=em)
#for getting nsfw images from the library
@bot.command()
async def nsfw(ctx, *args):
    if(ctx.guild is None and ctx.message.author != bot.user): #checks of user is trying to get past the nsfw filter
        await ctx.send("You Dumb stupid you are not allowed to use this command in dms")
    else:
        if(ctx.channel.is_nsfw()):#checks if the channel the command was sent from is nsfw
            query = ' '.join(args)
            #logic for getting a specific catagory form the catagory list
            if 'category' in query.lower() or 'categories' in query.lower():
                color = random.randrange(10000, 16777215, 1)
                for message in prawn.getCategoryMessages():
                    em = discord.Embed(description=message, color=color)
                    await ctx.send(embed=em)
            else: # logic for random catagory
                pu = ('Error', 'https://www.prajwaldesai.com/wp-content/uploads/2014/01/error-code.jpeg')
                if len(str(query)) <= 2:
                    pu = prawn.getRandom()
                else:
                    pu = prawn.getRandomLineFromQuery(query)
                print(pu)
                em = discord.Embed(description=pu[0], color=random.randrange(10000, 16777215, 1))  # 16777... is just FFFFFF in base10
                em.set_image(url=pu[1])
                await ctx.send(embed=em)
        else:
            await ctx.send("Sorry, but this command can only be used in a NSFW channel.")

#contact command
@bot.command()
async def contact(ctx):
    h = open("contact.txt", 'r')
    cont = h.read()
    h.close()
    del h

    msg = "Discord: Sai#2728\nDiscord server: https://discord.gg/gYhRdk7"
    if(ctx.channel.id == 674120261691506688):
        msg += cont
    id = ctx.message.author.id
    user = bot.get_user(id)
    channel = await user.create_dm()
    await channel.send(msg)

""""""""""""""""""""""""
"""Bot Admin Commands"""
""""""""""""""""""""""""

#for the admins to turn off the bot
@bot.command()
async def off(ctx):
    if(isOwner(ctx)):
        await ctx.send(msgReturn("offMsg"))
        await bot.logout()
        sys.exit(0)
    else:
        await ctx.send(msgReturn("notOwner"))

#for admins to admire shrek. Freezes the bot for a bit, so don't actually use
@bot.command()
async def shrek(ctx):
    if not isOwner(ctx):
        await ctx.send(msgReturn("notOwner"))
        return
    with open('Shrek.txt', 'r') as file: 
        lines = file.readlines()
        i = 0
        while i < len(lines):
            toSend = ''
            while len(toSend) < 1500 and i < len(lines): #Send 2000 chars
                if len(lines[i].lstrip()) > 1:
                    toSend = toSend +'\n'+ lines[i].lstrip()
                i = i + 1
            await ctx.send(toSend[1:]) #deletes leading newline (ewww what's fenceposting)

#gets the tempreture of the host pi
@bot.command()
async def temp(ctx):
    temp = os.popen("vcgencmd measure_temp").readline()
    await ctx.send(temp.replace("temp=",""))

#this allows the admins of the bot to send a message to ANY discord user
@bot.command()
async def sendDM(ctx, id: int, *, msg: str):
    if(isOwner(ctx)):
        user = bot.get_user(id)
        channel = await user.create_dm()
        await channel.send(msg)
    else:
        await ctx.send("An error as occurred, please do not contact me about it.")

#this allows the bot admins to change the status from the $help to something else
@bot.command()
async def status(ctx, type: str, *, other="https://twitch.tv/saiencevanadium/"):
    if(isOwner(ctx)):
        if(type.lower() == "stream"):
            await bot.change_presence(activity=discord.Streaming(name="Watching my creator", url=other))
        elif(type.lower() == "help"):
            await bot.change_presence(activity=discord.Game(name='with his food | $help'))
        elif(type.lower() == "music"):
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=other))
        elif(type.lower() == "watching"):
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=other))
    else:
        await ctx.send(msgReturn("notOwner"))


#runs the bot after all the methods have been loaded to memory
bot.run(TOKEN)
