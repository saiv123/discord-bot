import discord
intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.members = True

#all of the py libraires used
import sys, os, re
import traceback
import asyncio, discord
import wolframalpha
import time, datetime
from datetime import date
from datetime import datetime
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
from libraries.helperFunctions import isOwner, OwnersIgnoreCooldown, msgReturn, splitLongStrings, getEmbedsFromLibraryQuery, checkAuthSerers, add_to_embed
from libraries.helperFunctions import gen_rps_matrix, format_matrix, list_god
from libraries.helperFunctions import RgbToHex,HexToRgb
from libraries.prawn import getClosestFromList
from Levenshtein import distance

# for the math stuff
client = wolframalpha.Client(id)

# setting up the bot, with its discritpion etc.
bot = commands.Bot(command_prefix='$', description="Its a Sick use-less bot", intents=intents)
ts = time.time()

# setting up LyricGenius stuff
Gen = LyrGen.Genius(GenID)

# deleting default help comand
bot.remove_command('help')

######################################
###Inizalization of bot DO NOT EDIT###
######################################

#what the bot does on boot
@bot.event
async def on_ready():
    print('user: ' + bot.user.name)
    print('id: ' + str(bot.user.id))
    # setst the activity for the bot
    await bot.change_presence(activity=discord.Game(name='with his food | $help'))
    print('current time - ' + str(ts))
    print('-----------')

# for every message it does these checks
DEL_CMD = True
@bot.event
async def on_message(message):
    channel = message.channel
    if "456247671506599936" in message.content and message.author != bot.user:
        await channel.send("HEY! <@456247671506599936> YOUR MONTY FUCKING SUCKS <3~ ash aka motorcycle gal that loves ya")
    elif "corn" in message.content.lower() and message.author != bot.user:
        await channel.send("https://cdn.discordapp.com/attachments/654783232969277453/738997605039603772/Corn_is_the_best_crop__wheat_is_worst.mp4")
    elif "bird" in message.content.lower() and message.author != bot.user:
        await channel.send("The birds work for the bourgeoisie.")
    elif "nut" in message.content.lower() and message.author != bot.user:
        if(message.guild is None and message.author != bot.user):
            print("dm nut")
        else:
            if(channel.is_nsfw()):  # checks if the channel the command was sent from is nsfw
                await channel.send("https://cdn.discordapp.com/attachments/606355593887744013/726970883884711956/video0_1-8.mp4")
            else:
                print("not in nsfw channel")
    elif "pog" in message.content.lower() and message.author != bot.user and message.guild.id == 759462211818225684:
        await channel.send("https://tenor.com/view/oh-omg-fish-shookt-triggered-gif-9720855")

    # Respond to last command
    await bot.process_commands(message)

    # check if it responed to a command
    ran_cmd = message.content.startswith(bot.command_prefix) and message.content.split(' ')[0].strip(bot.command_prefix).lower() in [cmd.name.lower() for cmd in bot.commands]
    if DEL_CMD and ran_cmd: # Delete it if it can or should
        if message.guild.get_member(bot.user.id).permissions_in(message.channel).manage_messages:
            await message.delete()

#spits out the errors
@bot.event
async def on_command_error(ctx, error):
    msgSend = "An internal error has occured. Use $contact to contact the owner if it persists"
    if isinstance(error, commands.MissingRequiredArgument):
        e_msg = ', a '.join(str(error.param).replace('params','').split(':'))
        msgSend = f'You did not use the command correctly\nYou\'re missing {e_msg}\n\nIf you don\'t know how to use the command, use the $help command to see how to use all commands.'
    elif isinstance(error, commands.BadArgument):
        e_msg = ' and '.join(error.args)
        msgSend = f'You did not use the command correctly\nYou\'re arguements are wrong: {e_msg}\n\nIf you don\'t know how to use the command, use the $help command to see how to use all commands.'
    elif isinstance(error, commands.CommandOnCooldown):
        msgSend = 'You\'re on cooldown for '+ctx.invoked_with + '.\nPlease wait another '+str(round(error.retry_after))+' seconds'
    elif isinstance(error, commands.CommandNotFound):
        cmd = str(ctx.invoked_with)
        cmd_list = [cmd.name for cmd in bot.commands]
        mlo = getClosestFromList(cmd_list, cmd)
        if distance(cmd, mlo) <= 0.6*len(cmd):
            msgSend= f"Sorry, but that is not a valid command. Did you mean {mlo}?\n\nYou can add suggestions at [suggestions Website](https://github.com/saiv123/discord-bot/issues/new/choose)"
        else:
            msgSend = "Sorry but that is not a valid command\nYou can add suggestions at [suggestions Website](https://github.com/saiv123/discord-bot/issues/new/choose)"

    embeds = add_to_embed('Error','Command Entered: {}\n{}'.format(ctx.message.content, msgSend))
    for embed in embeds:
        embed.set_footer(text='Command Broken by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
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

    embed.set_footer(text='Help Requested by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)

#Gives you the github website link
@bot.command()
async def github(ctx):
    embed = discord.Embed(title= "GitHub Website for Bot",description="This is where you can see how the bot works",url="https://github.com/saiv123/discord-bot")
    embed.set_footer(text='Github Requested by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)

# will give you a link to invite the bot to other servers
@bot.command()
async def invite(ctx):
    embed = discord.Embed(colour=discord.Colour.green())
    embed.set_author(name='Invite the Bot to another server')
    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/314578387031162882/e4b98a4a9ca3315ca699ffe5cba5b8f1.png?size=1024')
    embed.add_field(name='Please invite me to other Discords',value='[Invite bot to server](https://discord.com/api/oauth2/authorize?client_id=314578387031162882&permissions=8&scope=bot)', inline=False)
    embed.set_footer(text='Invite Requested by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)

# magic 8 ball
@bot.command()
async def shouldI(ctx, *, msg:str):
    msg = " "+msg+" "
    # msg = ' '.join(msg)
    phrases = ['Yes! Go $','No, it won\'t work.','Hmmm, $ might be a fine idea','Unclear, consider rewording $','I don\'t know, ask someone else about $']
    embed = discord.Embed(title='Should I...', description='{}\n{}'.format(msg, random.choice(phrases).replace('$', msg)))
    embed.set_footer(text='Asked by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)

# says hello to your
@bot.command()
async def hi(ctx):
    await ctx.message.delete()
    await ctx.send("Hello {0}!!!".format(ctx.message.author.mention))

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
    # opens the file if the users file in there otherwise it will make it
    with open(nameNote, 'a') as file:
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        file.write(str(d1) + " -- " +notes + "\n")  # formating and saving to the file
    await ctx.send("{0.message.author.mention} Your Note is recorded and locked up.".format(ctx))
    del nameNote  # deletes the variable so it will free up some ram

# return the time the bot has been running
@bot.command()
async def stats(ctx):
    quote = quotes.getQuoteApi()
    # temp = os.popen("vcgencmd measure_temp").readline()

    # calculating time bot has been on
    tso = time.time()
    msg = time.strftime("%H Hours %M Minutes %S Seconds",time.gmtime(tso - ts))
    # seting up an embed
    embed = discord.Embed(colour=imgutils.randomSaturatedColor())
    # setting the clock image
    embed.set_thumbnail(url="https://hotemoji.com/images/dl/h/ten-o-clock-emoji-by-twitter.png")
    embed.add_field(name='I have been awake for:', value=msg, inline=True)
    # embed.add_field(name='My core body temperature:',value=temp.replace("temp=", ""), inline=True)
    embed.add_field(name='Quote cus I know you\'re bored:', value='"' +quote['quote'] + '"\n\t~' + quote['author'], inline=False)

    embed.set_footer(text='Status Requested by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
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
    res = list(res.results)

    embed=discord.Embed(title="Wolfram Aplha", description=func)
    embed.set_thumbnail(url="https://cdn.iconscout.com/icon/free/png-512/wolfram-alpha-2-569293.png")

    for i in range(len(res)):
        opener = True
        for msg in splitLongStrings(res[i].text, chars=1024):
            embed.add_field(name='Answer {}:'.format(i+1) if opener and len(res) > 1 else chr(0xffa0)*i+1,value=msg, inline=False)
            opener = False

    embed.set_footer(text='Answer Requested by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)

# sends a warming quote
@bot.command()
async def quote(ctx):
    quote = apis.quote_to_discord_embed(quotes.getQuoteJSON())
    quote.set_thumbnail(url='https://clipart.info/images/ccovers/1531011033heart-emoji.png')
    quote.set_footer(text='Quote Requested by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=quote)

# sends a random quote
@bot.command(cls=OwnersIgnoreCooldown)
@commands.cooldown(3, 60, commands.BucketType.user)
async def randquote(ctx):
    quote = quotes.getQuoteApi()
    embed = apis.quote_to_discord_embed(quote)
    embed.set_footer(text='Quote Requested by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)

# sends a random piece of advice
@bot.command(cls=OwnersIgnoreCooldown)
@commands.cooldown(3, 60, commands.BucketType.user)
async def advice(ctx):
    advice = apis.advice()
    embed = apis.quote_to_discord_embed(advice)
    embed.set_footer(text='Advice Requested by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)

# sends 2 stupid donald trump quotes and their contradiction score
@bot.command(cls=OwnersIgnoreCooldown)
@commands.cooldown(3, 60, commands.BucketType.user)
async def tronalddump(ctx):
    async with ctx.channel.typing():
        t = time.time()
        contra_tuple = apis.get_trump_contradiction()
        embeds = [apis.quote_to_discord_embed(i) for i in contra_tuple[1:]]

        nearest_contra_score = str(int(min(10,contra_tuple[0])))

        contra_meter = '0       1       2       3       4       5       6       7       8       9       10'.replace(nearest_contra_score, apis.number_to_discord_emote(nearest_contra_score))

        await asyncio.sleep(max(0, 2-(time.time()-t))) # wait a maximum of 2s. This command takes a lot of cpu
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
        embed.set_footer(text='Requested by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
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
                embed.set_footer(text='Requested by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Sorry',description='I\'m sorry {}, $nsfw can only be used in an NSFW channel'.format(ctx.message.author.name))
            embed.set_footer(text='Porn Requested by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)

# Contact command
@bot.command(cls=OwnersIgnoreCooldown)
@commands.cooldown(3, 60, commands.BucketType.user)
async def contact(ctx):
    msg = "Discord: Sai#3400\nDiscord server: <https://discord.gg/2zUTJ7j>\n"
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
        #splitting the stream to check if the input has a artist if not add by . to earch for the song name
        if ' by ' not in str(songName): songName = str(songName) + ' by '
        songName = str(songName).split(" by ")
        song = Gen.search_song(songName[0], songName[1])
        embed = discord.Embed(colour = imgutils.randomSaturatedColor())

        # Create and send embed
        for embed in add_to_embed(songName[0].title(), song.lyrics):
            embed.set_footer(text='Song Requested by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
    except AttributeError as e:
        print(e)
        embed = discord.Embed(title='Error in Song', description='The command was either used incorrectly or the song was not found\nCommand is used as follows: <b>$song songTitle by songArtist</b>')
        embed.set_footer(text='Song Requested by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

SPACE_LEN_HARD_CAP = 4000
@bot.command()
async def space(ctx, *, msg:str):
    # extract the first message from msg
    ints = re.findall(r'\d+',msg)
    if len(ints) > 0:
        space = int(ints[0])
        msg = re.sub(r'\s+','', msg.replace(str(space), ' '))
    else: space = 1

    exp_len = (len(msg)-1)*space + len(msg)
    if not isOwner(ctx) and exp_len >= SPACE_LEN_HARD_CAP:
        await ctx.send('That message would be {0} characters, waaaay higher than the limit of {1}. Chill.'.format(exp_len, SPACE_LEN_HARD_CAP))
        return

    to_send = (' '*max(1, space)).join(msg)
    for msg in splitLongStrings(to_send):
        await ctx.send(msg)



# rock paper scissors game with the bot (maybe buggy so no touchy)
RPS_HARD_CAP = 6
@bot.command()
async def rps(ctx, *, level=1):
    # local variables
    if level > RPS_HARD_CAP and not isOwner(ctx):
        msgs = add_to_embed('Level too high!', f'Sorry, but even though the code for it exists, why would you ever want to play rps-{level*2+1}???')
        for msg in msgs:
            msg.set_footer(text='RPS Played by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=msg)
        return

    symbol_names = ['rock','paper','scissors','spock','lizard','alien','well','generic','karen','heat','lemonade']
    # Extend symbol names if necessary
    for i in range(len(symbol_names), level*2+5):
        symbol_names.append('item'+str(i))

    # Generate matrix
    matrix = gen_rps_matrix(level)

    # Ask for user choice
    color = None
    for embed in add_to_embed(f'{ctx.message.author.name}\'s RPS','Pick an option:\nrules'+'\n'.join(symbol_names[:level*2+1])):
        color = embed.color
        await ctx.send(embed=embed)


    # Get user choice
    def check(m):
        return m.author == ctx.message.author and m.channel == ctx.message.channel

    try:
        msg = await bot.wait_for('message', check=check,timeout=1*60)
    except:
        embed = add_to_embed(f'{ctx.message.author.name}\'s RPS','Awww, don\'t leave me hangin\'')[0]
        embed.set_footer(text='RPS Played by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
        return
    freeform = msg.content.lower().replace(' ','_').replace('\n','')

    # Process winner
    mlo = getClosestFromList(['rules']+symbol_names,freeform)
    output = ''
    if 'rules' in mlo:
        output = ' \n'.join(format_matrix(matrix, symbol_names))
    elif distance(freeform, mlo) >= len(freeform)*0.3: #If the most likely option is more than 30% wrong, hassle
        output = 'No option recognized! Your choices are: '+'\n'.join(['rules']+symbol_names[:level*2+1])
    else:
        choice = symbol_names.index(getClosestFromList(symbol_names, freeform))
        computer_choice = random.randint(0, len(matrix[0])-1)

        winner = matrix[choice][computer_choice]
        if winner == 0:
            output = "Its a draw! Better luck next time"
        elif winner == 1:
            output = "You win. Nice job. 🥳"
        elif winner == 2:
            output = "I win ;) Better luck next time"
        output = output+"\n\nYou chose "+ symbol_names[choice]+"\nI chose "+symbol_names[computer_choice]

    for embed in add_to_embed(f'{ctx.message.author.name}\'s RPS', output):
        if color != None: embed.color = color
        embed.set_footer(text='RPS Played by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)



@bot.command()
async def rpsc(ctx, user:discord.User, *, level=1):
    # local variables
    if level > RPS_HARD_CAP and not isOwner(ctx):
        msgs = add_to_embed('Level too high!', f'Sorry, but even though the code for it exists, why would you ever want to play rps-{level*2+1}???')
        for msg in msgs:
            msg.set_footer(text='RPS Played by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=msg)
        return

    symbol_names = ['rock','paper','scissors','spock','lizard','alien','well','generic','karen','heat','lemonade']

    # Extend symbol names if necessary
    for i in range(len(symbol_names),level*2+5):
        symbol_names.append('item'+str(i))

    # Generate matrix
    matrix = gen_rps_matrix(level)

    msg = 'You are challenging '+user.name+' to rock-paper-scissors'
    if level > 1:
        msg = msg+'-'+str(level*2+1)

    for embed in add_to_embed(f'Your challenge to {user.name}',msg+'\nCheck your DMs!'):
        embed.set_footer(text='Challenge sent by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    def get_check(user):
        def check(msg):
            return msg.author == user and msg.channel == user.dm_channel
        return check

    async def get_response(_user, title='RPSC', timeout=10*60, opener=''):
        choice = symbol_names[0]
        i = 0
        while i < 3:
            i += 1
            for msg in add_to_embed(title, f'{opener}Your choices are '+', '.join(symbol_names[:2*level+1]+['rules','abort'])):
                await _user.send(embed=msg)
            opener = ''

            try:
                msg = await bot.wait_for('message', check=get_check(_user),timeout=timeout)
            except:
                await _user.send(embed=add_to_embed(title, f'Awww, {_user.name} don\'t leave me hangin\'')[0])
                return -1 # Abort challenge if you don't send an answer

            response = msg.content.lower().replace(' ','_').replace('\n','')
            choice = getClosestFromList(['abort','rules']+symbol_names,response.lower())
            if distance(response, choice) >= len(response)*0.3:
                await _user.send(embed=add_to_embed(choice, 'No option recognized, try again'))

            if 'abort' in choice.lower():
                return -1

            if 'rules' in choice.lower():
                for msg in add_to_embed(title, ' \n'.join(format_matrix(matrix, symbol_names))):
                    await _user.send(embed=msg)
                i -= 1
            else: # If neither rules or abort, it is correct
                break
        return choice


    # Get your response
    your_choice = await get_response(ctx.message.author, title=f'Your challenge to {user.name}')
    if your_choice == -1:
        await ctx.message.author.send(embed=add_to_embed(f'Your challenge to {user.name}', 'Challenge cancelled!')[0])
        await ctx.send(embed=add_to_embed(f'{ctx.message.author.name}\'s challenge', 'Challenge cancelled!')[0])
        return
    your_choice = symbol_names.index(your_choice)
    await ctx.message.author.send(embed=add_to_embed(f'Your challenge to {user.name}',f'You chose {symbol_names[your_choice]}')[0])

    # Get other person's response
    #await user.send(embed=add_to_embed('Rock-Paper-Scissors Challenge!', f'{ctx.message.author.name} has challenged you to rock-paper-scissors-'+str(level*2+1) if level > 1 else '')[0])
    enemy_choice = await get_response(user, title=f'{ctx.message.author.name}\'s challenge', opener=f'{ctx.message.author.name} has challenged you to rock-paper-scissors-'+str(level*2+1) if level > 1 else '')
    if enemy_choice == -1:
        embed = add_to_embed(f'{ctx.message.author.name}\'s challenge', 'Challenge cancelled!')[0]
        await user.send(embed=embed)
        await ctx.send(embed=embed)
        await ctx.message.author.send(embed=add_to_embed(f'Your challenge to {user.name}', 'Challenge cancelled by opponent')[0])
        return
    enemy_choice = symbol_names.index(enemy_choice)
    await user.send(embed=add_to_embed(f'{ctx.message.author.name}\'s challenge', f'You chose {symbol_names[enemy_choice]}')[0])

    msg = ""

    # Display results
    msg = f'{ctx.message.author.name} chose {symbol_names[your_choice]}'
    msg += f'\n{user.name} chose {symbol_names[enemy_choice]}'

    winner = matrix[enemy_choice][your_choice]
    if winner == 0:
        await ctx.message.author.send(embed=add_to_embed(f'Your challenge to {user.name}', msg.replace(ctx.message.author.name,'You')+'\nThe bout ended in a draw')[0])
        await user.send(embed=add_to_embed(f'{ctx.message.author.name}\'s challenge', msg.replace(user.name,'You')+'\nThe bout ended in a draw')[0])
        msg += '\nThe bout ended in a draw'
    elif winner == 1:
        await ctx.message.author.send(embed=add_to_embed(f'Your challenge to {user.name}', msg.replace(ctx.message.author.name,'You')+'\nYou won 🥳')[0])
        await user.send(embed=add_to_embed(f'{ctx.message.author.name}\'s challenge', msg.replace(user.name,'You')+'\nYou lost.')[0])
        msg += f'\n{ctx.message.author.name} won! 🥳'
    elif winner == 2:
        await ctx.message.author.send(embed=add_to_embed(f'Your challenge to {user.name}', msg.replace(ctx.message.author.name,'You')+'\nYou lost')[0])
        await user.send(embed=add_to_embed(f'{ctx.message.author.name}\'s challenge', msg.replace(user.name,'You')+'\nYou won 🥳')[0])
        msg += f'\n{user.name} won. Nice job. 🥳'

    for embed in add_to_embed(f'{ctx.message.author.name}\'s challenge', msg):
        embed.set_footer(text='RPS Played by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

@bot.command()
async def color(ctx, *, inputColor:str):
    try:
        color_dict = apis.getColor(inputColor)
        embed = apis.colorDictToEmbed(color_dict)
        embed.set_author(name="[See It Here]",url=color_dict['url'])
        embed.set_footer(text='Color picked by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)
    except ValueError:
        await ctx.send("The given color is incorrect. Enter it in Hex, RGB, or CMYK form")

@bot.command(cls=OwnersIgnoreCooldown)
@commands.cooldown(1, 30, commands.BucketType.user)
async def ping(ctx):
    embed = add_to_embed('Ping','Latency: {0}ms\nRound Trip Time: ??ms'.format(round(bot.latency*1000, 1)))[0]
    embed.set_footer(text='Ping Measured by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
    msg = await ctx.send(embed=embed)
    t = (msg.created_at - ctx.message.created_at).total_seconds() * 1000

    embed = add_to_embed('Ping','Latency: {}ms\nRound Trip Time: {}ms'.format(round(bot.latency*1000, 1), round(t, 1)))[0]
    embed.set_footer(text='Ping Measured by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
    await msg.edit(content=None, embed=embed)

@bot.command(cls=OwnersIgnoreCooldown)
@commands.cooldown(3, 15, commands.BucketType.user)
async def roll(ctx, *, dice="1d6"):
    dice = dice.upper()
    rolls = 1
    sides = 6
    print(dice)
    if(dice.find("D") == -1):
        try:
            rolls = int(dice)
        except ValueError as e:
            print("WITHOUT THE D")
            print(e)
            await ctx.send("Invalid Input")
            return
    else:
        try:
            rolls = int(dice[:dice.index("D")])
            sides = int(dice[dice.index("D")+1:])
        except ValueError as e:
            print("WITH THE D")
            print(e)
            await ctx.send("Invalid Input")
            return

    if(rolls <= 20 and rolls > 0 and sides > 1 and sides <= 100):
        randValues = []
        out = ""
        for i in range(rolls):
            randValues.append(random.randint(1,sides))
            out += randValues[i]+", "
        await ctx.send(out[:-2])
    else:
        await ctx.send("Sorry your inputs are invalid.\nPlease make sure you are rolling less than 20 times and have a dice that is lower than 100.")

    '''
    base cases -> roll d6 time 1 - when no input is given for roll
    if one number is given roll d6 time number input limit to 20
    if d# then roll once of for the dice size of #
    anyother case through an exception
    '''


###########################
###Server Admin Commands###
###########################

#give information on the user
@bot.command(aliases=["userstatus"])
async def userinfo(ctx):
    if ctx.author.guild_permissions.administrator or isOwner(ctx):
        x = ctx.guild.members
        if len(ctx.message.mentions) != 0:
             target = ctx.message.mentions[0]
             roles = [role for role in target.roles[1:]]
             embed = discord.Embed(title="User information", colour=discord.Color.gold(), timestamp= datetime.fromtimestamp(time.time()))
             embed.set_author(name=target.name, icon_url=target.avatar_url)
             embed.set_thumbnail(url=target.avatar_url)
             embed.set_footer(text='Info Requested by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

             #this checks if the user has no roles it will say they have no roles
             listRoles = "User has no roles"
             if len(roles) != 0:
                 listRoles = " ".join([role.mention for role in roles])

             fields = [("Name", str(target), False),
                   ("Status", target.raw_status, False),
                   (f"Roles ({len(roles)})", listRoles , False),
                   ("Created at", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), False),
                   ("Joined at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), False)]

             for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

             await ctx.send(embed=embed)
        else:
            await ctx.send(f'You have to ping someone from this server')
    else:
        await ctx.send(f'Not enough permissions')

#kick command
@bot.command()
async def kick(ctx):
    perms = ctx.author.guild_permissions
    if not (perms.administrator or perms.kick_members):
        await ctx.send("*One of us* doesn't have the permissions to do that...")
        return


    if len(ctx.message.mentions) <= 0:
        await ctx.send("You need to ping someone from this server to kick")
        return

    target = ctx.message.mentions[0]

    if not ctx.guild.get_member(bot.user.id).permissions_in(ctx.message.channel).kick_members or  ctx.guild.get_member(bot.user.id).roles[-1] <=  target.roles[-1]:
        await ctx.send("I don't have enough power to do that.")
        return

    canKick = True # I can't stand all these `if`s
    canKick = canKick and target.roles[-1] < ctx.author.roles[-1] # require a lesser role
    canKick = canKick and (not target.guild_permissions.administrator or target.bot) # can't kick admins (but can kick bot admins)
    if ctx.author.id == ctx.guild.owner_id: canKick = True # can't say no to the owners
    canKick = canKick and target.id != ctx.message.author.id # you can't kick yourself (even as an owner)

    if not canKick:
        await ctx.send("You cannot kick <@"+str(target.id)+"> \nthey have permissions higher than or equal to yours.")
        return

    # we can kick now
    msg = msgReturn("kick")
    await ctx.send(msg.format(target.name))
    print('Kicking')
    await target.kick()

#banning command
@bot.command()
async def ban(ctx):
    perms = ctx.author.guild_permissions
    if not (perms.administrator or perms.ban_members):
        await ctx.send("*One of us* doesn't have the permissions to do that...")
        return

    if len(ctx.message.mentions) <= 0:
        await ctx.send("You need to ping someone from this server to ban")
        return

    target = ctx.message.mentions[0]

    if not ctx.guild.get_member(bot.user.id).permissions_in(ctx.message.channel).kick_members or  ctx.guild.get_member(bot.user.id).roles[-1] <=  target.roles[-1]:
        await ctx.send("I don't have enough power to do that.")
        return

    canBan = True # I can't stand all these `if`s
    canBan = canBan and target.roles[-1] < ctx.author.roles[-1] # require a lesser role
    canBan = canBan and (not target.guild_permissions.administrator or target.bot) # can't ban admins (but can ban bot admins)
    if ctx.author.id == ctx.guild.owner_id: canBan = True # can't say no to the owners
    canBan = canBan and target.id != ctx.message.author.id # you can't ban yourself (even as an owner)

    if not canBan:
        await ctx.send("You cannot ban <@"+str(target.id)+"> \nthey have permissions higher than or equal to yours.")
        return

    # we can ban now
    msg = msgReturn("ban")
    await ctx.send(msg.format(target.name))
    print('Banning')
    await target.ban()

################################
###Commands to make you unsad###
################################

#up date to how the command will work, it will be limited to onnce ever 24 hours, but will always send the quote even if it does join the vc
#play / do something depending on if the user is in a voice channel or not
@bot.command(pass_context=True)
async def sad(ctx):
    user = bot.get_user(ctx.author.id)
    await user.send("Hey i see you have used the sad command, you are loved just know that :heart:")
    if checkAuthSerers(ctx):
        try:
            channel = ctx.author.voice.channel
            await channel.connect()

            #sends muic
            embed = add_to_embed('Time to unsad yourself','Music you can listen too:\n[Sad playlist 1](https://www.youtube.com/playlist?list=PLzSGJo-pe00ka90V3cFrEjCCJKROnHCMj)\n[Sad Playlist 2](https://www.youtube.com/playlist?list=PLzSGJo-pe00nNRlyDb8eJ4zSRXnAtevO6)\nHope you feel better from Sai.')[0]
            embed.set_footer(text='Unsading ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
            await ctx.send("https://tenor.com/view/hug-virtual-hug-hug-sent-gif-5026057")

            #leaving the voice channel
            await ctx.voice_client.disconnect()

        except AttributeError as e:
            #this is what it will do if user is not in vc
            print("user is not in a voice channel, reverting to text for unsadening user")
            quote = apis.quote_to_discord_embed(quotes.getQuoteJSON())
            quote.set_thumbnail(url='https://clipart.info/images/ccovers/1531011033heart-emoji.png')
            await ctx.send(embed=quote)
    else:
        #this is what it will do if user is not in trusted server
        quote = apis.quote_to_discord_embed(quotes.getQuoteJSON())
        quote.set_thumbnail(url='https://clipart.info/images/ccovers/1531011033heart-emoji.png')
        await ctx.send(embed=quote)

########################
###Bot Admin Commands###
########################

# for the admins to turn off the bot
@bot.command()
async def off(ctx):
    if(isOwner(ctx)):
        await ctx.send(msgReturn("offMsg"))
        await bot.close()

        sys.exit(0)
    else:
        await ctx.send(msgReturn("notOwner"))

# for admins to admire shrek. Freezes the bot for a bit, so don't actually use
@bot.command()
async def shrek(ctx, *, embed:bool=False):
    if not isOwner(ctx):
        await ctx.send(msgReturn("notOwner"))
        return
    with open('Shrek.txt', 'r') as file:
        shrek = file.read()
        if embed:
            for embed in add_to_embed('Shrek is love, Shrek is life', shrek.replace('\n\n','\n')):
                embed.color = discord.Colour(imgutils.randomSaturatedColor())
                await ctx.send(embed=embed)
        else:
            for message in splitLongStrings(shrek):
                await ctx.send(message.replace('\n\n','\n'))

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
    #cheks if your owner
    if isOwner(ctx):
        msg = ""
        #gets all the servers from bot object
        guilds = await bot.fetch_guilds(limit=150).flatten()
        msg = str(len(guilds)) + "\n"
        #loops through them and puts them in a string
        for i in guilds:
            msg += i.name + "\n"

        #creates a dm with user and dms it to them
        author = ctx.message.author
        await author.send(msg)
    else:
        await ctx.send(msgReturn("notOwner"))

# command will change offten to test out commands
@bot.command()
async def test(ctx):
    if not isOwner(ctx): return
    member = ctx.author
    print(dict(bot.intents))
    print(member.status)

# runs the bot after all the methods have been loaded to memory
bot.run(TOKEN)
