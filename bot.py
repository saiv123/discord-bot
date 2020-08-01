#all of the py libraires used
import sys, os
import asyncio, discord
import wolframalpha
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import time, datetime
import json, random

# external libraies
import quotes, prawn, imgutils
from secret import TOKEN, id, cont

# dir for the bots location
os.chdir("/home/pi/discord-bot")

# List of Owners/Bot admins
ownerId = [231957319737540608, 240636443829993473, 243774954955341828]

# for the math stuff
client = wolframalpha.Client(id)

# setting up the bot, with its discritpion etc.
bot = commands.Bot(command_prefix='$', description="Its a Sick use-less bot")
ts = time.time()

# deleting default help comand
bot.remove_command('help')

##########################
###bots helper commands###
##########################

# used as a check for some command so only the people that are allowed to use it can use it
def isOwner(ctx):
    for i in ownerId:
        if(ctx.author.id == i):
            return True
    return False

# gets a message from the dictionary with the type inputed
def msgReturn(type):
    data = json.load(open("msg.json"))
    typeM = data[type]
    msgData = random.choice(typeM)
    del data, typeM
    return msgData

# Splits a string into several sub-2000 char strings
def splitLongStrings(str, chars=1500):
    messages = []
    if ' ' not in str:  # If there are no spaces, don't respect spaces
        message = ""
        for c in str:
            if len(message) >= chars:  # >= is equivalent to adding 1 to len(message)
                messages.append(message)
                message = ""
            message = message + c
        messages.append(message)
        return messages
    # If there are spaces, respect them
    words = str.split(' ')
    message = ""
    for word in words:
        if len(message) + len(word) > chars:
            messages.append(message[1:])  # delete leading space
            message = ""
        message = message + ' ' + word
    if len(message) > 1:
        messages.append(message[1:])
    return messages

# Gets embed responses from a library of links
def getEmbedsFromLibraryQuery(libraryPath, query):
    # If query is categories, get categories
    if 'category' in query.lower() or 'categories' in query.lower():
        color = imgutils.randomSaturatedColor()
        embeds = []
        for message in splitLongStrings(' '.join(prawn.getCategoryMessages(path=libraryPath))):
            embeds.append(discord.Embed(description=message, color=color))
        return embeds
    # Otherwise, get image from query
    namedImg = (
        'Error', 'https://www.prajwaldesai.com/wp-content/uploads/2014/01/error-code.jpeg')

    # Iterate up to 5x to try and get a valid image
    for i in range(5):
        if len(str(query)) <= 2:
            namedImg = prawn.getRandom(path=libraryPath)
        else:
            namedImg = prawn.getRandomLineFromQuery(query, path=libraryPath)
        if imgutils.isUrlValidImage(namedImg[1]):
            break
    if not imgutils.isUrlValidImage(namedImg[1]):  # Print error
        print('Image not valid at ' +
              namedImg[1] + '\n\t(name ' + namedImg[0] + ')')

    embed = discord.Embed(description=namedImg[0], color=imgutils.getAverageColor(
        namedImg[1]))  # 16777... is just FFFFFF in base10
    embed.set_image(url=namedImg[1])
    return [embed]

######################################
###Inizalization of bot DO NOT EDIT###
######################################

# you may think that this function
# is obslete, and doesnt seem to do
# anything. and you would be correct.
# but when we remove this function
# for some reason the whole bot
# does not work/launch properly
# and cant figure out why,
# so here it will stay.
#  no touchy

@bot.event
async def on_ready():
    print('user: ' + bot.user.name)
    print('id: ' + str(bot.user.id))
    # setst the activity for the bot
    await bot.change_presence(activity=discord.Game(name='with his food | $help'))
    print('current time - ' + str(ts))
    print('-----------')

# for every message it does these checks
@bot.event
async def on_message(message):
    nameNote = "dmLogs.txt"
    # if(message.author.id is 371865866704257025 and message.guild != None): #for removing user from servers
    #     await message.delete()
    #     return
    if message.guild is None and message.author != bot.user:  # checks if theres a dm to the bot, and logs it
        other = await bot.fetch_user(message.author.id)
        with open(nameNote, 'a') as file:
            file.write(str(datetime.datetime.now()) + " " +
                       other.name + " -- " + message.content + "\n")
    elif "corn" in message.content.lower():
        channel = message.channel
        await channel.send("https://cdn.discordapp.com/attachments/654783232969277453/738997605039603772/Corn_is_the_best_crop__wheat_is_worst.mp4")

    # Respond to last command
    await bot.process_commands(message)

##############
###Commands###
##############

# our curtom help command
@bot.command(pass_context=True)
async def help(ctx):
    # seting up an embed
    embed = discord.Embed(
        colour=discord.Colour.green()
    )

    embed.set_author(name='Help')
    embed.set_thumbnail(
        url='https://cdn.discordapp.com/avatars/314578387031162882/e4b98a4a9ca3315ca699ffe5cba5b8f1.png?size=1024')
    embed.add_field(name='Commands will be found on the website.',
                    value='[Link to website](https://saiv123.github.io/discord-bot/website/)', inline=False)
    embed.add_field(name='Please invite me to other discords',
                    value='[Invite bot to server](https://discordapp.com/api/oauth2/authorize?client_id=314578387031162882&permissions=402730064&scope=bot)', inline=False)

    await ctx.send(embed=embed)

#magic 8 ball
@bot.command()
async def shouldI(ctx, *i):
    i = ' '.join(i)
    phrases = ['Yes! Go $','No, it won\'t work.','Hmmm, $ might be a fine idea','Unclear, consider rewording $','I don\'t know, ask someone else about $']
    await ctx.send(random.choice(phrases).replace('$', i))

# will give you a link to invite the bot to other servers
@bot.command()
async def invite(ctx):
    async with ctx.channel.typing():  # make it look like the bot is typing
        time.sleep(3)
        await ctx.send("Invite me to your friends disocrd:\nhttps://discordapp.com/api/oauth2/authorize?client_id=314578387031162882&permissions=402730064&scope=bot")


# says hello to your
@bot.command()
async def hi(ctx):
    await ctx.message.delete()
    user = ("<@" + str(ctx.message.author.id) + "> ")
    await ctx.send("Hello " + user + "!!!!!!!")

# for the user to see their notes
@bot.command()
async def getnotes(ctx):
    try:
        notes = ""
        nameNote = ("MyPorn/" + str(ctx.author.id) + ".txt")
        f = open(nameNote, "r")
        temp = f.readlines()
        lineNums = len(temp)

        # will loop and get the last 5 notes saved
        if(lineNums <= 5):
            for i in temp:
                notes += str(i)
        else:
            for i in range(lineNums - 5, lineNums):
                notes += str(temp[i])
        for message in splitLongStrings(notes):
            await ctx.author.send(message)
    except IOError:  # edge case if the user does not have any notes / file
        print("File Not Found")
        await ctx.author.send("You do not have any notes")

# removes the personal files
@bot.command()
async def deletenotes(ctx):
    nameNote = ('MyPorn/' + str(ctx.author.id) + '.txt')
    command = 'sudo rm -r ' + nameNote
    os.system(command)
    await ctx.send("Your Personal Notes have been Destroyed")

# logic for saving their notes
@bot.command()
async def notes(ctx, *, notes=" "):
    nameNote = ("MyPorn/" + str(ctx.author.id) + ".txt")
    # deletes the users message so others dont see what they saved
    await ctx.message.delete()
    user = ("<@" + str(ctx.message.author.id) + "> ")
    # opens the file if the users file in there otherwise it will make it
    with open(nameNote, 'a') as file:
        file.write(str(datetime.datetime.now()) + " -- " +
                   notes + "\n")  # formating and saving to the file
    await ctx.send(user + "Your Note is recorded and locked up.")
    del nameNote  # deletes the variable so it will free up some ram

# return the time the bot has been running
@bot.command()
async def stats(ctx):
    quote, author = quotes.getQuoteApi()
    temp = os.popen("vcgencmd measure_temp").readline()

    # calculating time bot has been on
    tso = time.time()
    msg = time.strftime("%H Hours %M Minutes %S Seconds",
                        time.gmtime(tso - ts))
    # random color for embed
    color = random.randrange(10000, 16777215, 1)
    # seting up an embed
    embed = discord.Embed(colour=color)
    # setting the clock image
    embed.set_thumbnail(
        url="https://hotemoji.com/images/dl/h/ten-o-clock-emoji-by-twitter.png")
    embed.add_field(name='I have been awake for:', value=msg, inline=False)
    embed.add_field(name='My core body tempreture:',
                    value=temp.replace("temp=", ""), inline=False)
    embed.add_field(name='Quote cus I know your bored:', value='"' +
                    str(quote) + '"\n ~' + str(author), inline=False)
    async with ctx.channel.typing():  # make it look like the bot is typing
        time.sleep(3)
        await ctx.send(embed=embed)

# return the answers to defenet integrals
@bot.command()
async def definte(ctx, a: int, b: int, func: str):
    # bunch of text formating to put into the api
    res = client.query('integrate ' + func + ' from ' +
                       str(a) + ' to ' + str(b))
    # getting the answer from the api and parsing
    await ctx.send(next(res.results).text)

# sends a warming quote
@bot.command()
async def quote(ctx):
    async with ctx.channel.typing():
        time.sleep(3)
        await ctx.send(quotes.formatQuote(text=quotes.getQuoteJSON()[0] + " :heart:"))

# sends a random quote
@bot.command()
async def randquote(ctx):
    async with ctx.channel.typing():
        time.sleep(3)
        quote, author = quotes.getQuoteApi()
        await ctx.send(quotes.formatQuote(text=quote, author=author))

# For getting memes from the library
memePath = 'ClassWork/'
@bot.command()
async def meme(ctx, *args):
    query = ' '.join(args)
    for embed in getEmbedsFromLibraryQuery(memePath, query):
        await ctx.send(embed=embed)

# for getting nsfw images from the library
prawnPath = 'MyHomework/'
@bot.command()
async def nsfw(ctx, *args):
    # checks of user is trying to get past the nsfw filter
    if(ctx.guild is None and ctx.message.author != bot.user):
        await ctx.send("You Dumb stupid you are not allowed to use this command in dms")
    else:
        if(ctx.channel.is_nsfw()):  # checks if the channel the command was sent from is nsfw
            query = ' '.join(args)
            for embed in getEmbedsFromLibraryQuery(prawnPath, query):
                await ctx.send(embed=embed)
        else:
            await ctx.send("Sorry, but this command can only be used in a NSFW channel.")

# Contact command
@bot.command()
async def contact(ctx):
    msg = "Discord: Sai#2728\nDiscord server: https://discord.gg/gYhRdk7\n"
    if(ctx.channel.id == 674120261691506688):  # channel specific to my discord server
        msg += cont
    id = ctx.message.author.id
    # Making the dm channel
    user = bot.get_user(id)
    await user.send(msg)

# rock paper scissors game with the bot (some what buggy so no touchy)
@bot.command()
async def rps(ctx, *args):
    # local variables
    user = ("<@" + str(ctx.message.author.id) + "> ")
    output = ""
    msg = ''.join(args)
    msg.lower()  # making the input lower case
    correct = False
    opt = ["rock", "paper", "scissors"]

    # to test if the input is one of the options
    for i in opt:
        if (i == msg):
            correct = True

    # a waird edge case where if the input was null, it would some how pass the last test and correct would be true
    if(msg == ''):
        correct = False
    if(not correct):
        output = (
            "Somthing went worng the command is used like\n$rps [rock,paper,or scissors]")
    else:
        # chose a random option from the opt list
        randC = opt[random.randint(0, 2)]
        if(randC == msg):
            output = ("Its a draw! Better luck next time\nBot: " +
                      randC + " " + user + ": " + msg)
        elif(randC == "rock"):
            if(msg == "paper"):
                output = ("You win. Nice job. :partying_face:\nBot: " +
                          randC + " " + user + ": " + msg)
            else:
                output = ("I win ;) Better luck next time\nBot: " +
                          randC + " " + user + ": " + msg)
        elif(randC == "paper"):
            if(msg == "scissors"):
                output = ("You win. Nice job. :partying_face:\nBot: " +
                          randC + " " + user + ": " + msg)
            else:
                output = ("I win ;) Better luck next time\nBot: " +
                          randC + " " + user + ": " + msg)
        else:
            if(msg == "rock"):
                output = ("You win. Nice job. :partying_face:\nBot: " +
                          randC + " " + user + ": " + msg)
            else:
                output = ("I win ;) Better luck next time\nBot: " +
                          randC + " " + user + ": " + msg)
    await ctx.send(output)

########################
###Bot Admin Commands###
########################

# for the admins to turn off the bot
@bot.command()
async def off(ctx):
    if(isOwner(ctx)):
        await ctx.send(msgReturn("offMsg"))
        await bot.logout()
        sys.exit(0)
    else:
        await ctx.send(msgReturn("notOwner"))

# for admins to admire shrek. Freezes the bot for a bit, so don't actually use
@bot.command()
async def shrek(ctx):
    if not isOwner(ctx):
        await ctx.send(msgReturn("notOwner"))
        return
    with open('Shrek.txt', 'r') as file:
        shrek = file.read()
        for message in splitLongStrings(shrek):
            await ctx.send(message)

# this allows the admins of the bot to send a message to ANY discord user
@bot.command()
async def sendDM(ctx, id: int, *, msg: str):
    if(isOwner(ctx)):
        user = bot.get_user(id)
        await user.send(msg)
    else:
        await ctx.send(msgReturn("notOwner"))

# this allows the bot admins to change the status from the $help to something else
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

# send you the servers the bot is in
@bot.command()
async def servers(ctx):
    if isOwner(ctx):
        msg = ""
        guilds = await bot.fetch_guilds(limit=150).flatten()
        msg = str(len(guilds)) + "\n"
        for i in guilds:
            msg += i.name + "\n"

        author = ctx.message.author
        await author.send(msg)
    else:
        await ctx.send(msgReturn("notOwner"))

# to test what the bot see in the object containers
@bot.command()
async def sendbot(ctx, temp:str):
    if isOwner(ctx):
        await ctx.send("\\"+temp)
    else:
        await ctx.send(mesgReturn("notOwner"))

# runs the bot after all the methods have been loaded to memory
bot.run(TOKEN)
