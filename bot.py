#all of the py libraires used
import sys, os
import asyncio, discord
import wolframalpha
import time, datetime
import json, random
from discord.ext import commands, tasks
from discord.ext.commands import Bot

# external libraies
import quotes
import helperFunctions
from secret import TOKEN, id, cont
from helperFunctions import isOwner, msgReturn, splitLongStrings, getEmbedsFromLibraryQuery
from prawn import getClosestFromList
from Levenshtein import distance

# dir for the bots location
os.chdir("/home/pi/discord-bot")

# for the math stuff
client = wolframalpha.Client(id)

# setting up the bot, with its discritpion etc.
bot = commands.Bot(command_prefix='$', description="Its a Sick use-less bot")
ts = time.time()

# deleting default help comand
bot.remove_command('help')

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
    elif "corn" in message.content.lower() and message.author != bot.user:
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
    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/314578387031162882/e4b98a4a9ca3315ca699ffe5cba5b8f1.png?size=1024')
    embed.add_field(name='Commands will be found on the website.',value='[Link to website](https://saiv123.github.io/discord-bot/website/)', inline=False)
    embed.add_field(name='Please invite me to other discords',value='[Invite bot to server](https://discordapp.com/api/oauth2/authorize?client_id=314578387031162882&permissions=402730064&scope=bot)', inline=False)

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
async def rps(ctx, *, level:int=1):
    # local variables
    user = ("<@" + str(ctx.message.author.id) + "> ")
    freeform = freeform.lower().replace(' ','_').replace('\n','')

    symbol_names = ['rock','paper','scissors','spock','lizard','alien','well','generic','karen','heat','lemonade']
    # Extend symbol names if necessary
    for i in range(len(symbol_names),level*2+5):
        symbol_names.append('item'+i)

    # RPS helper methods
    def gen_rps_matrix(size):
        row = [0] + [i%2+1 for i in range(2*size)] # baseline rps winner matrix 0 1 2 1 2 ...
        matrix = [row]
        for i in range(2*size):
            row = row[-1:] + row[:-1] # right shift 2 0 1 2 1 ....
            matrix.append(row)
        return matrix
    def format_matrix(matrix, symbol_names):
        lines = list()
        for p1 in range(len(matrix)):
            for p2 in range(p1+1, len(matrix[p1])):
                winner_symbol = p2 if matrix[p1][p2] == 1 else p1
                loser_symbol = p1 if matrix[p1][p2] == 1 else p2
                lines.append(str(list_god(symbol_names,winner_symbol,'Nothing'))+' beats '+str(list_god(symbol_names,loser_symbol,'nothing')))
        return lines
    def list_god(list, index, default): # list_get_or_default, nothing to do with religion
        return (list[index:index+1]+[default])[0]

    # Generate matrix
    matrix = gen_rps_matrix(level)

    # Get user choice
    def check(m):
        return m.author is ctx.message.author
    msg = await client.wait_for('message', check=check,timeout=30)
    print('recieved raw msg: '+str(msg))
    if msg is None:
        await ctx.send('Awww, don\'t leave me hangin\'')
        return
    freeform = msg.content
    print('recieved msg: '+str(freeform))

    mlo = getClosestFromList(['rules']+symbol_names,freeform)
    if 'rules' in mlo:
        for msg in splitLongStrings(' \n'.join(format_matrix(matrix, symbol_names))):
            await ctx.send(msg)
    elif distance(freeform, mlo) >= len(freeform)*0.3: #If the most likely option is more than 30% wrong, hassle
        await ctx.send('No option recognized! Your choices are: ')
        for msg in splitLongStrings('\n '.join(['rules']+symbol_names[:level*2+1])):
            await ctx.send(msg)
    else:
        choice = symbol_names.index(getClosestFromList(symbol_names, freeform))
        computer_choice = random.randint(0, len(matrix[0])-1)

        winner = matrix[choice][computer_choice]
        if winner == 0:
            output = "Its a draw! Better luck next time"
        elif winner == 1:
            output = "You win. Nice job. :partying_face:"
        elif winner == 2:
            output = "I win ;) Better luck next time"
        output = output+"\n\nYou chose "+ symbol_names[choice]+"\nI chose "+symbol_names[computer_choice]
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
