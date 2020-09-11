#all of the py libraires used
import sys, os
import traceback
import asyncio, discord
import wolframalpha
import time, datetime
import json, random
import lyricsgenius as LyrGen
from discord.ext import commands, tasks
from discord.ext.commands import Bot

# external libraies
import libraries.quotes as quotes
import libraries.helperFunctions as helperFunctions
import libraries.bonusapis as apis
import libraries.imgutils as imgutils

from secret import TOKEN, id, cont, GenID
from libraries.helperFunctions import isOwner, OwnersIgnoreCooldown, msgReturn, splitLongStrings, getEmbedsFromLibraryQuery
from libraries.helperFunctions import gen_rps_matrix, format_matrix, list_god
from libraries.helperFunctions import RgbToHex,HexToRgb
from libraries.prawn import getClosestFromList
from Levenshtein import distance

# dir for the bots location
os.chdir("/home/pi/discord-bot")

# for the math stuff
client = wolframalpha.Client(id)

# setting up the bot, with its discritpion etc.
bot = commands.Bot(command_prefix='$', description="Its a Sick use-less bot")
ts = time.time()

#setting up LyricGenius stuff
Gen = LyrGen.Genius(GenID)

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
    #nameNote = "dmLogs.txt"
    # if(message.author.id is 371865866704257025 and message.guild != None): #for removing user from servers
    #     await message.delete()
    #     return
    # if message.guild is None and message.author != bot.user:  # checks if theres a dm to the bot, and logs it
    #     other = await bot.fetch_user(message.author.id)
    #     with open(nameNote, 'a') as file:
    #         file.write(str(datetime.datetime.now()) + " " +other.name + " -- " + message.content + "\n")
    if "corn" in message.content.lower() and message.author != bot.user:
        channel = message.channel
        await channel.send("https://cdn.discordapp.com/attachments/654783232969277453/738997605039603772/Corn_is_the_best_crop__wheat_is_worst.mp4")
    elif "bird" in message.content.lower() and message.author != bot.user:
        channel = message.channel
        await channel.send("The birds work for the bourgeoisie.")

    # Respond to last command
    await bot.process_commands(message)

#spits out the errors
@bot.event
async def on_command_error(ctx, error):
    msgSend = "An internal error has occured. Use $contact to contact the owner if it persists"
    if isinstance(error, commands.MissingRequiredArgument):
        msgSend = 'You did not use the command correctly\nArguments: '+str(error.args)+'\nIf you dont know how to use the command, use the $help command\nto see how to use all commands.'
        print('arg' + str(error.args))
        print('params' + str(error.param))
    elif isinstance(error, commands.CommandOnCooldown):
        msgSend = 'You\'re on cooldown for '+ctx.invoked_with + '.\nPlease wait another '+str(round(error.retry_after))+' seconds'
    elif isinstance(error, commands.CommandNotFound):
        cmd = str(ctx.invoked_with)
        cmd_list = [cmd.name for cmd in bot.commands]
        mlo = getClosestFromList(cmd_list, cmd)
        if distance(cmd, mlo) <= 0.4*len(cmd):
            msgSend="Sorry, but that is not a valid command. Did you mean "+mlo+"?\n\nYou can add suggestions at https://github.com/saiv123/discord-bot/issues/new/choose"
        else:
            msgSend = "Sorry but that is not a valid command\nYou can add suggestions at https://github.com/saiv123/discord-bot/issues/new/choose"

    await ctx.send(msgSend)
    print(error)
    print(traceback.format_exc()) # Attempt to print exception

##############
###Commands###
##############

# our curtom help command
@bot.command(pass_context=True)
async def help(ctx):
    # seting up an embed
    embed = discord.Embed(description="Info on the bot and how to use it",colour=discord.Colour.green())

    embed.set_author(name='Help')
    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/314578387031162882/e4b98a4a9ca3315ca699ffe5cba5b8f1.png?size=1024')
    embed.add_field(name='Commands will be found on the website.',value='[Link to website](https://saiv123.github.io/discord-bot/website/)', inline=False)
    embed.add_field(name='Please invite me to other Discords',value='[Invite bot to server](https://discord.com/api/oauth2/authorize?client_id=314578387031162882&permissions=8&scope=bot)', inline=False)

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
        await ctx.send("Invite me to your friend's Discord:\nhttps://discord.com/api/oauth2/authorize?client_id=314578387031162882&permissions=8&scope=bot")

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
        file.write(str(datetime.datetime.now()) + " -- " +notes + "\n")  # formating and saving to the file
    await ctx.send(user + "Your Note is recorded and locked up.")
    del nameNote  # deletes the variable so it will free up some ram

# return the time the bot has been running
@bot.command()
async def stats(ctx):
    async with ctx.channel.typing():  # make it look like the bot is typing
        quote = quotes.getQuoteApi()
        temp = os.popen("vcgencmd measure_temp").readline()

        #calculating time bot has been on
        tso = time.time()
        msg = time.strftime("%H Hours %M Minutes %S Seconds",time.gmtime(tso - ts))
        #random color for embed
        color = random.randrange(10000, 16777215, 1)
        #seting up an embed
        embed = discord.Embed(colour=color)
        #setting the clock image
        embed.set_thumbnail(url="https://hotemoji.com/images/dl/h/ten-o-clock-emoji-by-twitter.png")
        embed.add_field(name='I have been awake for:', value=msg, inline=False)
        embed.add_field(name='My core body temperature:',value=temp.replace("temp=", ""), inline=False)
        embed.add_field(name='Quote cus I know you\'re bored:', value='"' +quote['quote'] + '"\n\t~' + quote['author'], inline=False)

        await ctx.send(embed=embed)

# return the answers to defenet integrals
@bot.command(cls=OwnersIgnoreCooldown)
@commands.cooldown(3, 60, commands.BucketType.user)
async def definte(ctx, a:int, b:int, *, func:str):
    # bunch of text formating to put into the api
    res = client.query('integrate ' + func + ' from ' +str(a) + ' to ' + str(b))
    # getting the answer from the api and parsing
    await ctx.send(next(res.results).text)

@bot.command(cls=OwnersIgnoreCooldown)
@commands.cooldown(3, 60, commands.BucketType.user)
async def wolfram(ctx, *, func:str):
    res = client.query(func)
    res = next(res.results).text

    embed=discord.Embed(title="Wolfram Aplha", description=func+':\n'+res)
    embed.set_thumbnail(url="https://cdn.iconscout.com/icon/free/png-512/wolfram-alpha-2-569293.png")
    await ctx.send(embed=embed)

# sends a warming quote
@bot.command()
async def quote(ctx):
    async with ctx.channel.typing():
        quote = apis.quote_to_discord_embed(quotes.getQuoteJSON())
        quote.set_thumbnail(url='https://clipart.info/images/ccovers/1531011033heart-emoji.png')
        await ctx.send(embed=quote)

# sends a random quote
@bot.command(cls=OwnersIgnoreCooldown)
@commands.cooldown(3, 60, commands.BucketType.user)
async def randquote(ctx):
    async with ctx.channel.typing():
        quote = quotes.getQuoteApi()
        await ctx.send(embed=apis.quote_to_discord_embed(quote))

# sends a random piece of advice
@bot.command(cls=OwnersIgnoreCooldown)
@commands.cooldown(3, 60, commands.BucketType.user)
async def advice(ctx):
    async with ctx.channel.typing():
        advice = apis.advice()
        await ctx.send(embed=apis.quote_to_discord_embed(advice))

# sends 2 stupid donald trump quotes and their contradiction score
@bot.command(cls=OwnersIgnoreCooldown)
@commands.cooldown(3, 60, commands.BucketType.user)
async def tronalddump(ctx):
    async with ctx.channel.typing():
        contra_tuple = apis.get_trump_contradiction()
        embeds = [apis.quote_to_discord_embed(i) for i in contra_tuple[1:]]

        nearest_contra_score = str(int(min(10,contra_tuple[0])))

        contra_meter = '0       1       2       3       4       5       6       7       8       9       10'.replace(nearest_contra_score, apis.number_to_discord_emote(nearest_contra_score))

        await ctx.send('For educational and mockery purposes only!')
        for embed in embeds:
            await ctx.send(embed=embed)
        await ctx.send('Contradiction Score:\n'+contra_meter+'\nScore: '+str(contra_tuple[0]))

# For getting memes from the library
memePath = 'ClassWork/'
@bot.command(cls=OwnersIgnoreCooldown)
@commands.cooldown(3, 60, commands.BucketType.user)
async def meme(ctx, *args):
    query = ' '.join(args)
    for embed in getEmbedsFromLibraryQuery(memePath, query):
        await ctx.send(embed=embed)

# for getting nsfw images from the library
prawnPath = 'MyHomework/'
@bot.command(cls=OwnersIgnoreCooldown)
@commands.cooldown(3, 60, commands.BucketType.user)
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
@bot.command(cls=OwnersIgnoreCooldown)
@commands.cooldown(3, 60, commands.BucketType.user)
async def contact(ctx):
    msg = "Discord: Sai#3400\nDiscord server: https://discord.gg/2zUTJ7j\n"
    if(ctx.channel.id == 674120261691506688):  # channel specific to my discord server
        msg += cont
    id = ctx.message.author.id
    # Making the dm channel
    user = bot.get_user(id)
    await user.send(msg)

#Get song lyrics
@bot.command(cls=OwnersIgnoreCooldown)
@commands.cooldown(1, 30, commands.BucketType.user)
async def song(ctx, *, songName:str):
    try:
        async with ctx.channel.typing():
            #splitting the stream to check if the input has a artist if not add by . to earch for the song name
            if ' by ' not in str(songName): songName = str(songName) + ' by '
            songName = str(songName).split(" by ")
            song = Gen.search_song(songName[0], songName[1])
            embed = discord.Embed(colour = imgutils.randomSaturatedColor())

            # Create and send embed
            embed.set_author(name=songName[0].title())
            for message in splitLongStrings(song.lyrics, chars=1024, preferred_char='\n'):
                embed.add_field(name=chr(0xffa0),value=message, inline=False)
            embed.set_footer(text='Song Requested by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
    except AttributeError as e:
        print(e)
        await ctx.send("The command was either used incorrectly or the song was not found\nCommand is used like:```$song songTitle by songArtist```")

# rock paper scissors game with the bot (maybe buggy so no touchy)
RPS_HARD_CAP = 6
@bot.command()
async def rps(ctx, *, level=1):
    # local variables
    user = ("<@" + str(ctx.message.author.id) + "> ")
    if level > RPS_HARD_CAP and not isOwner(ctx):
        await ctx.send(user+'Sorry, but even though the code for it exists, why would you ever want to play rps-'+str(level*2+1)+'???')
        return
    symbol_names = ['rock','paper','scissors','spock','lizard','alien','well','generic','karen','heat','lemonade']
    # Extend symbol names if necessary
    for i in range(len(symbol_names),level*2+5):
        symbol_names.append('item'+str(i))

    # Generate matrix
    matrix = gen_rps_matrix(level)

    # Ask for user choice
    for msg in splitLongStrings(user+': Pick an option.\nrules. '+', '.join(symbol_names[:level*2+1])):
            await ctx.send(msg)

    # Get user choice
    def check(m):
        return m.author is ctx.message.author and m.channel == ctx.message.channel

    try:
        msg = await bot.wait_for('message', check=check,timeout=30)
    except:
        await ctx.send('Awww, '+user+' don\'t leave me hangin\'')
        return
    freeform = msg.content.lower().replace(' ','_').replace('\n','')

    # Process winner
    mlo = getClosestFromList(['rules']+symbol_names,freeform)
    if 'rules' in mlo:
        for msg in splitLongStrings(' \n'.join(format_matrix(matrix, symbol_names))):
            await ctx.send(msg)
    elif distance(freeform, mlo) >= len(freeform)*0.3: #If the most likely option is more than 30% wrong, hassle
        for msg in splitLongStrings('No option recognized! Your choices are: '+', '.join(['rules']+symbol_names[:level*2+1])):
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

@bot.command()
async def rpsc(ctx, user:discord.User, *, level=1):
    # local variables
    if level > RPS_HARD_CAP and not isOwner(ctx):
        await ctx.send(user+'Sorry, but even though the code for it exists, why would you ever want to play rps-'+str(level*2+1)+', let alone with someone else???')
        return
    symbol_names = ['rock','paper','scissors','spock','lizard','alien','well','generic','karen','heat','lemonade']
    # Extend symbol names if necessary
    for i in range(len(symbol_names),level*2+5):
        symbol_names.append('item'+str(i))
    # Generate matrix
    matrix = gen_rps_matrix(level)

    msg = 'You are challending '+user.name+' to rock-paper-scissors'
    if level > 1:
        msg = msg+'-'+str(level*2+1)
    await ctx.send(msg+'\nCheck your DMs!')

    def get_check(user):
        def check(msg):
            return msg.author == user and msg.channel == user.dm_channel
        return check

    # Get your response
    your_choice = symbol_names[0]
    i = 0
    while i < 3:
        i += 1
        for msg in splitLongStrings('Your choices are '+', '.join(symbol_names[:2*level+1]+['rules','abort'])):
            await ctx.message.author.send(msg)
        try:
            msg = await bot.wait_for('message', check=get_check(ctx.message.author),timeout=5*60)
        except:
            await ctx.message.author.send('Awww, '+user.name+' don\'t leave me hangin\'')
            return # Abort challenge if you don't send an answer
        response = msg.content.lower().replace(' ','_').replace('\n','')
        your_choice = getClosestFromList(['abort','rules']+symbol_names,response.lower())

        if distance(response, your_choice) >= len(response)*0.3:
            await ctx.message.author.send('No option recognized, try again')

        if 'abort' in your_choice.lower():
            await ctx.message.author.send('Challenge cancelled')
            await ctx.send(ctx.message.author.name+' has cancelled the challenge')
            return

        if 'rules' in your_choice.lower():
            for msg in splitLongStrings(' \n'.join(format_matrix(matrix, symbol_names))):
                await user.send(msg)
            i -= 1
        else: # If neither rules or abort, it is correct
            break

    await ctx.message.author.send('You chose '+str(your_choice))

    # Get other person's response
    enemy_choice = symbol_names[0]
    await user.send(str(ctx.message.author.name)+' has challenged you to rock-paper-scissors'+('-'+str(level*2+1) if level > 1 else ''))
    i = 0
    while i < 3:
        i += 1
        for msg in splitLongStrings('Your choices are '+', '.join(symbol_names[:2*level+1]+['rules','abort'])):
            await user.send(msg)
        try:
            msg = await bot.wait_for('message', check=get_check(user),timeout=5*60)
        except:
            await user.send('Challenge cancelled')
            await ctx.message.author.send('Your opponent has cancelled the challenge')
            await ctx.send(user.name+' has cancelled the challenge')
            return # Consider breaking and leaving it at default instead of cancelling
        response = msg.content.lower().replace(' ','_').replace('\n','')
        enemy_choice = getClosestFromList(['abort','rules']+symbol_names,response.lower())

        if distance(response, enemy_choice) >= len(response)*0.3:
            await user.send('No option recognized, try again')

        if 'abort' in enemy_choice.lower():
            await user.send('Challenge cancelled')
            await ctx.message.author.send('Your opponent has cancelled the challenge')
            await ctx.send(user.name+' has cancelled the challenge')
            return

        if 'rules' in enemy_choice.lower():
            for msg in splitLongStrings(' \n'.join(format_matrix(matrix, symbol_names))):
                await user.send(msg)
            i -= 1
        else: # If neither rules or abort, it is correct
            break

    await user.send('You chose '+str(enemy_choice))

    # Display results
    await ctx.send(ctx.message.author.name+' chose '+your_choice)
    await ctx.send(user.name+' chose '+enemy_choice)

    # Calculate and display winner
    your_choice = symbol_names.index(your_choice)
    enemy_choice = symbol_names.index(enemy_choice)

    #winner = matrix[your_choice][enemy_choice]
    winner = matrix[enemy_choice][your_choice]
    if winner == 0:
        output = "Its a draw! What a sad conclusion..."
        await ctx.message.author.send('The bout ended in a draw')
        await user.send('The bout ended in a draw')
    elif winner == 1:
        output = ctx.message.author.name+" won. Nice job. :partying_face:"
        await ctx.message.author.send('You won! :partying_face:')
        await user.send('You lost')
    elif winner == 2:
        output = user.name+" won. Nice job. :partying_face:"
        await ctx.message.author.send('You lost')
        await user.send('You won! :partying_face:')
    await ctx.send(output)

@bot.command()
async def color(ctx, *inputColor):
    if(inputColor[0][0] == "#"):
        if(len(inputColor[0].lstrip('#'))%3 == 0 and len(inputColor[0].lstrip('#')) < 7): #checks if its a valid hex color value
            if len(inputColor[0].lstrip("#")) == 3:
                temp = inputColor[0].lstrip("#")
                out = ""
                for c in temp:
                    out += c*2
                inputColor[0] = "#"+out

            rgb = HexToRgb(inputColor[0])
            embed = discord.Embed(colour=int(inputColor[0].lstrip("#"), 16)) #converts the hex color value(str) to a hex number
            embed.add_field(name="Hex",value=inputColor[0], inline=True)
            embed.add_field(name="RGB",value=rgb, inline=True)
            embed.set_author(name="[Website for the Color]",url="https://www.color-hex.com/color/"+inputColor[0].lstrip("#"))
            embed.set_footer(text='Color picked by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("The hex color vlaue inputed was not properly formated, like this #FFF or #FFFFFF")
    elif(len(inputColor) == 3):
        for i in inputColor:
            if(int(i)>255 or int(i)<0):
                await ctx.send("The RGB vlues are not correct the RGB vlues have to be between 0 and 255")
                return #to send the loop because the numbers are wrong
        #converting hex string to hex number value
        hexS = RgbToHex(int(inputColor[0]),int(inputColor[1]),int(inputColor[2]))
        hexI = int(hexS.lstrip("#"), 16)
        #discord embed setup
        embed = discord.Embed(colour=hexI)
        embed.add_field(name="Hex",value=hexS, inline=True)
        embed.add_field(name="RGB",value='({})'.format(', '.join(inputColor)), inline=True)
        embed.set_author(name="[Website for the Color]",url="https://www.color-hex.com/color/"+hexS.lstrip("#"))
        embed.set_footer(text='Color picked by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        raise commands.MissingRequiredArgument
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
        await ctx.send(msgReturn("notOwner"))

# runs the bot after all the methods have been loaded to memory
bot.run(TOKEN)
