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
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

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

# The guild ID of the test server. Remove when done testing
guild_ids = [272155212347736065, 648012188685959169, 504049573694668801]

# for the math stuff
client = wolframalpha.Client(id)

# setting up the bot, with its discritpion etc.
bot = commands.Bot(command_prefix='/', description="Its a Sick use-less bot", intents=intents)
slash = SlashCommand(bot, sync_commands=True)
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
    await bot.change_presence(activity=discord.Game(name='with his food | /help'))
    print('current time - ' + str(ts))
    print('-----------')

# for every message it does these checks
AUTORESPOND = True
@bot.event
async def on_message(message):
    channel = message.channel

    if "456247671506599936" in message.content and message.author != bot.user:
        await channel.send("HEY! <@456247671506599936> YOUR MONTY FUCKING SUCKS <3~ ash aka motorcycle gal that loves ya")
    elif AUTORESPOND and "corn" in message.content.lower() and message.author != bot.user:
        await channel.send("https://cdn.discordapp.com/attachments/654783232969277453/738997605039603772/Corn_is_the_best_crop__wheat_is_worst.mp4")
    elif AUTORESPOND and "bird" in message.content.lower() and message.author != bot.user:
        await channel.send("The birds work for the bourgeoisie.")
    
    # Respond to last command
    await bot.process_commands(message)

# Currently does not work due to slash commands
#spits out the errors
@bot.event
async def on_command_error(ctx, error):
    msgSend = "An internal error has occured. Use /contact to contact the owner if it persists"
    if isinstance(error, commands.MissingRequiredArgument):
        e_msg = ', a '.join(str(error.param).replace('params','').split(':'))
        msgSend = f'You did not use the command correctly\nYou\'re missing {e_msg}\n\nIf you don\'t know how to use the command, use the /help command to see how to use all commands.'
    elif isinstance(error, commands.BadArgument):
        e_msg = ' and '.join(error.args)
        msgSend = f'You did not use the command correctly\nYou\'re arguements are wrong: {e_msg}\n\nIf you don\'t know how to use the command, use the /help command to see how to use all commands.'
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

@slash.slash(name='help', description='Give you help', guild_ids=guild_ids)
async def help(ctx):
    # seting up an embed
    embed = discord.Embed(description="Info on the bot and how to use it",colour=discord.Colour.green())

    embed.set_author(name='Help')
    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/314578387031162882/e4b98a4a9ca3315ca699ffe5cba5b8f1.png?size=1024')
    embed.add_field(name='Commands will be found on the website.',value='[Link to website](https://saiv123.github.io/discord-bot/website/)', inline=False)
    embed.add_field(name='Please invite me to other Discords',value='[Invite bot to server](https://discord.com/api/oauth2/authorize?client_id=314578387031162882&permissions=8&scope=bot)', inline=False)

    embed.set_footer(text='Help Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

#Gives you the github website link
@slash.slash(name='github', description='See the github!', guild_ids=guild_ids)
async def github(ctx):
    embed = discord.Embed(title= "GitHub Website for Bot",description="This is where you can see how the bot works",url="https://github.com/saiv123/discord-bot")
    embed.set_footer(text='Github Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

# will give you a link to invite the bot to other servers
@slash.slash(name='invite', description='Add me to your server!', guild_ids=guild_ids)
async def invite(ctx):
    embed = discord.Embed(colour=discord.Colour.green())
    embed.set_author(name='Invite the Bot to another server')
    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/314578387031162882/e4b98a4a9ca3315ca699ffe5cba5b8f1.png?size=1024')
    embed.add_field(name='Please invite me to other Discords',value='[Invite bot to server](https://discord.com/api/oauth2/authorize?client_id=314578387031162882&permissions=8&scope=bot)', inline=False)
    embed.set_footer(text='Invite Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

# magic 8 ball
@bot.command()
async def shouldI(ctx, *, msg:str):
    msg = " "+msg+" "
    # msg = ' '.join(msg)
    phrases = ['Yes! Go $','No, it won\'t work.','Hmmm, $ might be a fine idea','Unclear, consider rewording "/"','I don\'t know, ask someone else about $']
    embed = discord.Embed(title='Should I...', description='{}\n{}'.format(msg, random.choice(phrases).replace('/', msg)))
    embed.set_footer(text='Asked by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

# says hello to your
@slash.slash(name='hi', description='Am I here? Are you here? Is anyone really here?', guild_ids=guild_ids)
async def hi(ctx):
    embed = discord.Embed(title='Hello', description='Hello {0}!!!'.format(ctx.author.mention))
    embed.set_footer(text='Sanity check by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

# for the user to see their notes
@slash.slash(name='getnotes', description='Gets your notes', guild_ids=guild_ids)
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
    
    embed = discord.Embed(title='Notes Retrieved')
    embed.set_footer(text='Notes used by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

# removes the personal files
@slash.slash(name='deletenotes', description='Deletes your notes', guild_ids=guild_ids)
async def deletenotes(ctx):
    nameNote = ('MyPorn/' + str(ctx.author.id) + '.txt')
    command = 'sudo rm -r ' + nameNote
    os.system(command)
    await ctx.send('Your Personal Notes have been destroyed')

# logic for saving their notes
@slash.slash(name='note',
    description='Take a note!',
    options=[
        create_option(
            name='memory',
            description='What I will record',
            option_type=3,
            required=True
        )
    ],
    guild_ids=guild_ids
)
async def notes(ctx, memory:str=''):
    nameNote = ("MyPorn/" + str(ctx.author.id) + ".txt")

    # opens the file if the users file in there otherwise it will make it
    with open(nameNote, 'a') as file:
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        file.write(str(d1) + " -- " +memory + "\n")  # formating and saving to the file
    await ctx.send('Your Note is recorded and locked up.', hidden=True) # hides the users message so others dont see what they saved

# return the time the bot has been running
@slash.slash(name='stats', description='What am I up to?', guild_ids=guild_ids)
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

    embed.set_footer(text='Status Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

# return the answers to defenet integrals
# TODO: add cooldown of 60s every 3 commands
@slash.slash(name='definte',
    description='Calculate a definite integral',
    options=[
        create_option(
            name='func',
            description='The function to integrate',
            option_type=3,
            required=True
        ),
        create_option(
            name='a',
            description='Integral lower bound',
            option_type=3,
            required=True
        ),
        create_option(
            name='b',
            description='Integral upper bound',
            option_type=3,
            required=True
        )
    ],
    guild_ids=guild_ids
)
async def definte(ctx, a:int=0, b:int=0, func:str=''):
    # bunch of text formating to put into the api
    res = client.query('integrate ' + func + ' from ' +str(a) + ' to ' + str(b))
    # getting the answer from the api and parsing
    await ctx.send(next(res.results).text)

# TODO: add cooldown of 60s every 3 commands
@slash.slash(name='wolfram',
    description='Calculate anything!',
    options=[
        create_option(
            name='query',
            description='What should I ask?',
            option_type=3,
            required=True
        )
    ],
    guild_ids=guild_ids
)
async def wolfram(ctx, query:str=''):
    res = client.query(query)
    res = list(res.results)

    embed=discord.Embed(title="Wolfram Aplha", description=query)
    embed.set_thumbnail(url="https://cdn.iconscout.com/icon/free/png-512/wolfram-alpha-2-569293.png")

    for i in range(len(res)):
        opener = True
        for msg in splitLongStrings(res[i].text, chars=1024):
            embed.add_field(name='Answer {}:'.format(i+1) if opener and len(res) > 1 else chr(0xffa0)*i+1,value=msg, inline=False)
            opener = False

    embed.set_footer(text='Answer Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

# sends a warming quote
@slash.slash(name='quote', description='Sends a heartwarming quote', guild_ids=guild_ids)
async def quote(ctx):
    quote = apis.quote_to_discord_embed(quotes.getQuoteJSON())
    quote.set_thumbnail(url='https://clipart.info/images/ccovers/1531011033heart-emoji.png')
    quote.set_footer(text='Quote Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=quote)

# sends a random quote
# TODO: add cooldown of 60s for each 3 uses
@slash.slash(name='randquote', description='Get a unique quote', guild_ids=guild_ids)
async def randquote(ctx):
    quote = quotes.getQuoteApi()
    embed = apis.quote_to_discord_embed(quote)
    embed.set_footer(text='Quote Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

# sends a random piece of advice
# TODO: add cooldown of 60s for each 3 uses
@slash.slash(name='advice', description='Sends a random piece of advice', guild_ids=guild_ids)
async def advice(ctx):
    advice = apis.advice()
    embed = apis.quote_to_discord_embed(advice)
    embed.set_footer(text='Advice Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

# sends 2 stupid donald trump quotes and their contradiction score
# TODO: add cooldown of 60s for each 3 uses
# TODO: completely broken rn
@slash.slash(name='tronalddump', description='Sends 2 stupid trump quotes and attemps to gauge the difference', guild_ids=guild_ids)
async def tronalddump(ctx):
    t = time.time()
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
# TODO: add cooldown of 60s for each 3 uses
@slash.slash(name='meme',
    description='Get a meme!',
    options=[
        create_option(
            name='query',
            description='Any special requests?',
            option_type=3,
            required=False
        )
    ],
    guild_ids=guild_ids
)
async def meme(ctx, query:str=''):
    embed = getEmbedsFromLibraryQuery(memePath, query)[0]
    embed.set_footer(text='Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

# for getting nsfw images from the library
prawnPath = 'MyHomework/'
# TODO: add cooldown of 60s for each 3 uses
@slash.slash(name='nsfw',
    description='Get some nono pics',
    options=[
        create_option(
            name='query',
            description='Any special requests?',
            option_type=3,
            required=False
        )
    ],
    guild_ids=guild_ids
)
async def nsfw(ctx, query:str=''):
    # checks of user is trying to get past the nsfw filter
    if(ctx.guild is None and ctx.author != bot.user):
        await ctx.send("You Dumb stupid you are not allowed to use this command in dms")
    else:
        if(ctx.channel.is_nsfw()):  # checks if the channel the command was sent from is nsfw
            embed = getEmbedsFromLibraryQuery(prawnPath, query)[0]
            embed.set_footer(text='Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Sorry',description='I\'m sorry {}, /nsfw can only be used in an NSFW channel'.format(ctx.author.name))
            embed.set_footer(text='Porn Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

# Contact command
@slash.slash(name='contact', description='Contact my father', guild_ids=guild_ids)
async def contact(ctx):
    msg = "Discord: Sai#3400\nDiscord server: <https://discord.gg/2zUTJ7j>\n"
    if(ctx.channel.id == 674120261691506688):  # channel specific to my discord server
        msg += cont
    id = ctx.author.id
    # Making the dm channel
    user = bot.get_user(id)
    await user.send(msg)

#Get song lyrics
# TODO: add cooldown of 30s for each 1 use
@slash.slash(name='song',
    description='Grab a song\'s lyrics',
    options=[
        create_option(
            name='song',
            description='The title of the song',
            option_type=3,
            required=True
        )
    ],
    guild_ids=guild_ids
)
async def song(ctx, song:str=''):
    try:
        #splitting the stream to check if the input has a artist if not add by . to earch for the song name
        if ' by ' not in str(song): song = str(song) + ' by '
        song = str(song).split(" by ")
        songInfo = Gen.search_song(song[0], song[1])
        embed = discord.Embed(title=song[0].title(), colour = imgutils.randomSaturatedColor())

        # Create and send embed
        for e in add_to_embed(embed, songInfo.lyrics):
            e.set_footer(text='Song Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=e)
    except AttributeError as e:
        print(e)
        embed = discord.Embed(title='Error in Song', description='The command was either used incorrectly or the song was not found\nCommand is used as follows: <b>/song songTitle by songArtist</b>')
        embed.set_footer(text='Song Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

SPACE_LEN_HARD_CAP = 4000
@slash.slash(name='space',
    description='Spread a message',
    options=[
        create_option(
            name='message',
            description='What\'s gotta be spread',
            option_type=3,
            required=True
        ),
        create_option(
            name='amount',
            description='What\'s gotta be spread',
            option_type=4,
            required=False
        ),
    ],
    guild_ids=guild_ids
)
async def space(ctx, message:str='', amount:int=1):
    exp_len = (len(message)-1)*amount + len(message)
    if not isOwner(ctx) and exp_len >= SPACE_LEN_HARD_CAP:
        await ctx.send('That message would be {0} characters, waaaay higher than the limit of {1}. Chill.'.format(exp_len, SPACE_LEN_HARD_CAP))
        return

    to_send = (' '*max(1, amount)).join(message)
    for message in splitLongStrings(to_send):
        await ctx.send(message)



# rock paper scissors game with the bot (maybe buggy so no touchy)
# Does not currently work with slash commands
RPS_HARD_CAP = 6
@slash.slash(name='rps',
    description='Play rock-paper-scissors',
    options=[
        create_option(
            name='level',
            description='Add more symbols to the classic game',
            option_type=4,
            required=False
        )
    ],
    guild_ids=guild_ids
)
async def rps(ctx, *, level=1):
    if level > RPS_HARD_CAP and not isOwner(ctx):
        msg = add_to_embed('Level too high!', f'Sorry, but even though the code for it exists, why would you ever want to play rps-{level*2+1}???')[0]
        msg.set_footer(text='RPS Played by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
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

    embed = add_to_embed(f'{ctx.author.name}\'s RPS','Pick an option:\nrules'+'\n'.join(symbol_names[:level*2+1]))[0]
    color = embed.color
    await ctx.send(embed=embed)


    # Get user choice
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', check=check,timeout=1*60)
    except:
        embed = add_to_embed(f'{ctx.author.name}\'s RPS','Awww, don\'t leave me hangin\'')[0]
        embed.set_footer(text='RPS Played by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)
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

    embed = add_to_embed(f'{ctx.author.name}\'s RPS', output)[0]
    if color != None: embed.color = color
    embed.set_footer(text='RPS Played by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)



@slash.slash(name='rpsc',
    description='Play rock-paper-scissors',
    options=[
        create_option(
            name='user',
            description='Ping who you want to challenge',
            option_type=6,
            required=False
        ),
        create_option(
            name='level',
            description='Add more symbols to the classic game',
            option_type=4,
            required=False
        )
    ],
    guild_ids=guild_ids
)
async def rpsc(ctx, user:discord.User=None, level:int=1):
    if level > RPS_HARD_CAP and not isOwner(ctx):
        msg = add_to_embed('Level too high!', f'Sorry, but even though the code for it exists, why would you ever want to play rps-{level*2+1}???')[0]
        msg.set_footer(text='RPS Played by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
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

    embed = add_to_embed(f'Your challenge to {user.name}',msg+'\nCheck your DMs!')[0]
    embed.set_footer(text='Challenge sent by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
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
    your_choice = await get_response(ctx.author, title=f'Your challenge to {user.name}')
    if your_choice == -1:
        await ctx.author.send(embed=add_to_embed(f'Your challenge to {user.name}', 'Challenge cancelled!')[0])
        await ctx.channel.send(embed=add_to_embed(f'{ctx.author.name}\'s challenge', 'Challenge cancelled!')[0])
        return
    your_choice = symbol_names.index(your_choice)
    await ctx.author.send(embed=add_to_embed(f'Your challenge to {user.name}',f'You chose {symbol_names[your_choice]}')[0])

    # Get other person's response
    #await user.send(embed=add_to_embed('Rock-Paper-Scissors Challenge!', f'{ctx.message.author.name} has challenged you to rock-paper-scissors-'+str(level*2+1) if level > 1 else '')[0])
    enemy_choice = await get_response(user, title=f'{ctx.author.name}\'s challenge', opener=f'{ctx.author.name} has challenged you to rock-paper-scissors-'+str(level*2+1) if level > 1 else '')
    if enemy_choice == -1:
        embed = add_to_embed(f'{ctx.author.name}\'s challenge', 'Challenge cancelled!')[0]
        await user.send(embed=embed)
        await ctx.channel.send(embed=embed)
        await ctx.author.send(embed=add_to_embed(f'Your challenge to {user.name}', 'Challenge cancelled by opponent')[0])
        return
    enemy_choice = symbol_names.index(enemy_choice)
    await user.send(embed=add_to_embed(f'{ctx.author.name}\'s challenge', f'You chose {symbol_names[enemy_choice]}')[0])

    msg = ""

    # Display results
    msg = f'{ctx.author.name} chose {symbol_names[your_choice]}'
    msg += f'\n{user.name} chose {symbol_names[enemy_choice]}'

    winner = matrix[enemy_choice][your_choice]
    if winner == 0:
        await ctx.author.send(embed=add_to_embed(f'Your challenge to {user.name}', msg.replace(ctx.author.name,'You')+'\nThe bout ended in a draw')[0])
        await user.send(embed=add_to_embed(f'{ctx.author.name}\'s challenge', msg.replace(user.name,'You')+'\nThe bout ended in a draw')[0])
        msg += '\nThe bout ended in a draw'
    elif winner == 1:
        await ctx.author.send(embed=add_to_embed(f'Your challenge to {user.name}', msg.replace(ctx.author.name,'You')+'\nYou won 🥳')[0])
        await user.send(embed=add_to_embed(f'{ctx.author.name}\'s challenge', msg.replace(user.name,'You')+'\nYou lost.')[0])
        msg += f'\n{ctx.author.name} won! 🥳'
    elif winner == 2:
        await ctx.author.send(embed=add_to_embed(f'Your challenge to {user.name}', msg.replace(ctx.author.name,'You')+'\nYou lost')[0])
        await user.send(embed=add_to_embed(f'{ctx.author.name}\'s challenge', msg.replace(user.name,'You')+'\nYou won 🥳')[0])
        msg += f'\n{user.name} won. Nice job. 🥳'

    embed = add_to_embed(f'{ctx.author.name}\'s challenge to {user.name}', msg)[0]
    embed.set_footer(text='RPS Played by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

# TODO: add cooldown of 60s after 3 calls
@slash.slash(name='color',
    description='Get information about a color',
    options=[
        create_option(
            name='input',
            description='A color as hex, rgb, or cmyk',
            option_type=3,
            required=True
        )
    ],
    guild_ids=guild_ids
)
async def color(ctx, input:str=''):
    try:
        color_dict = apis.getColor(input)
        embed = apis.colorDictToEmbed(color_dict)
        embed.set_author(name="[See It Here]",url=color_dict['url'])
        embed.set_footer(text='Color picked by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)
    except ValueError:
        await ctx.send("The given color is incorrect. Enter it in Hex, RGB, or CMYK form")

@slash.slash(name='ping', description='What\'s my speed?', guild_ids=guild_ids)
async def ping(ctx):
    embed = add_to_embed('Ping','Latency: {0}ms\nRound Trip Time: ??ms'.format(round(bot.latency*1000, 1)))[0]
    embed.set_footer(text='Ping Measured by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
    msg = await ctx.send(embed=embed)
    t = (msg.created_at - ctx.created_at).total_seconds() * 1000

    embed = add_to_embed('Ping','Latency: {}ms\nRound Trip Time: {}ms'.format(round(bot.latency*1000, 1), round(t, 1)))[0]
    embed.set_footer(text='Ping Measured by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
    await msg.edit(content=None, embed=embed)

@slash.slash(name='roll',
    description='Roll a dice',
    options=[
        create_option(
            name='dice',
            description='The type of dice or compound dice',
            option_type=3,
            required=False
        )
    ],
    guild_ids=guild_ids
)
async def roll(ctx, dice:str='1d6'):
    MAXROLLS = 20
    MAXSIDES = 100
    dice = dice.upper()
    r_data = []

    print(dice)

    async def senderr(msg=''):
        msg = f'\n{msg}' if len(msg) > 0 else ''
        embed = discord.Embed(title='Input was Invalid', description=f'The command was used incorrectly it is used like `/roll` or `/roll 2d4`{msg}')
        embed.set_footer(text=f'Command used inproperly by: {ctx.author.name} (args: {dice})', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    def rollone(rolls, sides):
        total, txt = 0, ""
        for i in range(rolls):
            x = random.randint(1,sides)
            txt += f'{x}, '
            total += x
        return total, txt[:-2] if rolls > 0 else ""

    if(dice.find('D') == -1):
        try:
            r_data = [int(dice), 6]
        except ValueError:
            await senderr()
            return
    else:
        try:
            r_data = [int(x) for x in dice.split('D')]
        except ValueError:
            await senderr()
            return

    dice = 'd'.join([str(x) for x in r_data])
    grand_total, msg = 0, ''
    while len(r_data) > 1:
        rolls, sides = r_data[:2]

        if 0 < rolls <= MAXROLLS and 1 < sides <= MAXSIDES:
            total, out = rollone(rolls, sides)
            grand_total += total

            out = f'{rolls}d{sides}: {out}'

            # add dice total on if this isn't the last iteration
            if len(r_data) > 2 and rolls > 1: out = f'{out} (total: {total})'

            # add to msg with fenceposting
            msg = f'{msg}\n{out}' if len(msg) > 0 else out

            # shorten list
            r_data.pop(0)
            r_data[0] = total
        else:
            await senderr(f'{msg}\nYou have reached the limits. Make sure you roll less than {MAXROLLS} dice and each dice has less than {MAXSIDES} sides')
            return

    embed = discord.Embed(title=str(dice), description=f'{msg}\n\nTotal: {total}', colour=imgutils.randomSaturatedColor())
    embed.set_footer(text=f'{dice} was rolled by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

###########################
###Server Admin Commands###
###########################

#give information on the user
@slash.slash(name='userinfo',
    description='Pull a user\'s info. Admin only',
    options=[
        create_option(
            name='user',
            description='Ping the person',
            option_type=6,
            required=True
        )
    ],
    guild_ids=guild_ids
)
async def userinfo(ctx, user:discord.User=None):
    if not ctx.author.guild_permissions.administrator and not isOwner(ctx):
        await ctx.send(f'You must be an owner or a server administrator', hidden=True)
        return
    x = ctx.guild.members
    roles = [role for role in user.roles[1:]]
    embed = discord.Embed(title="User information", colour=discord.Color.gold(), timestamp= datetime.fromtimestamp(time.time()))
    embed.set_author(name=user.name, icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    embed.set_footer(text='Info Requested by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)

    #this checks if the user has no roles it will say they have no roles
    listRoles = "User has no roles"
    if len(roles) != 0:
        listRoles = " ".join([role.mention for role in roles])

    fields = [("Name", str(user), False),
        ("Status", user.raw_status, False),
        (f"Roles ({len(roles)})", listRoles , False),
        ("Created at", user.created_at.strftime("%d/%m/%Y %H:%M:%S"), False),
        ("Joined at", user.joined_at.strftime("%d/%m/%Y %H:%M:%S"), False)]

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    await ctx.send(embed=embed)        

#kick command
@slash.slash(name='kick',
    description='Kicks someone. Admin only',
    options=[
        create_option(
            name='user',
            description='Ping the person',
            option_type=6,
            required=True
        )
    ],
    guild_ids=guild_ids
)
async def kick(ctx, user:discord.User=None):
    perms = ctx.author.guild_permissions
    if not (perms.administrator or perms.kick_members):
        await ctx.send("*One of us* doesn't have the permissions to do that...")
        return

    if user == None:
        await ctx.send("You need to ping someone from this server to kick")
        return

    if not ctx.guild.get_member(bot.user.id).permissions_in(ctx.channel).kick_members or  ctx.guild.get_member(bot.user.id).roles[-1] <=  target.roles[-1]:
        await ctx.send("I don't have enough power to do that.")
        return

    canKick = True # I can't stand all these `if`s
    canKick = canKick and user.roles[-1] < ctx.author.roles[-1] # require a lesser role
    canKick = canKick and (not user.guild_permissions.administrator or user.bot) # can't kick admins (but can kick bot admins)
    if ctx.author.id == ctx.guild.owner_id: canKick = True # can't say no to the owners
    canKick = canKick and user.id != ctx.author.id # you can't kick yourself (even as an owner)

    if not canKick:
        await ctx.send("You cannot kick <@"+str(user.id)+"> \nthey have permissions higher than or equal to yours.")
        return

    # we can kick now
    msg = msgReturn("kick")
    await ctx.send(msg.format(user.name))
    print('Kicking')
    await user.kick()

#banning command
@slash.slash(name='ban',
    description='Bans someone. Admin only',
    options=[
        create_option(
            name='user',
            description='Ping the person',
            option_type=6,
            required=True
        )
    ],
    guild_ids=guild_ids
)
async def ban(ctx, user:discord.User=None):
    perms = ctx.author.guild_permissions
    if not (perms.administrator or perms.ban_members):
        await ctx.send("*One of us* doesn't have the permissions to do that...")
        return

    if user == None:
        await ctx.send("You need to ping someone from this server to ban")
        return

    if not ctx.guild.get_member(bot.user.id).permissions_in(ctx.channel).kick_members or  ctx.guild.get_member(bot.user.id).roles[-1] <=  target.roles[-1]:
        await ctx.send("I don't have enough power to do that.")
        return

    canBan = True # I can't stand all these `if`s
    canBan = canBan and user.roles[-1] < ctx.author.roles[-1] # require a lesser role
    canBan = canBan and (not user.guild_permissions.administrator or user.bot) # can't ban admins (but can ban bot admins)
    if ctx.author.id == ctx.guild.owner_id: canBan = True # can't say no to the owners
    canBan = canBan and user.id != ctx.author.id # you can't ban yourself (even as an owner)

    if not canBan:
        await ctx.send("You cannot ban <@"+str(user.id)+"> \nthey have permissions higher than or equal to yours.")
        return

    # we can ban now
    msg = msgReturn("ban")
    await ctx.send(msg.format(user.name))
    print('Banning')
    await user.ban()

################################
###Commands to make you unsad###
################################

#up date to how the command will work, it will be limited to onnce ever 24 hours, but will always send the quote even if it does join the vc
#play / do something depending on if the user is in a voice channel or not
@slash.slash(name='sad', description='Makes you unsad', guild_ids=guild_ids)
async def sad(ctx):
    user = bot.get_user(ctx.author.id)
    await user.send("Hey i see you have used the sad command, you are loved just know that :heart:")
    if checkAuthSerers(ctx):
        try:
            channel = ctx.author.voice.channel
            await channel.connect()

            #sends muic
            embed = add_to_embed('Time to unsad yourself','Music you can listen too:\n[Sad playlist 1](https://www.youtube.com/playlist?list=PLzSGJo-pe00ka90V3cFrEjCCJKROnHCMj)\n[Sad Playlist 2](https://www.youtube.com/playlist?list=PLzSGJo-pe00nNRlyDb8eJ4zSRXnAtevO6)\nHope you feel better from Sai.')[0]
            embed.set_footer(text='Unsading ' + ctx.author.name, icon_url=ctx.author.avatar_url)
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
@slash.slash(name='off', description='Kills me. Owner only', guild_ids=guild_ids)
async def off(ctx):
    if(isOwner(ctx)):
        await ctx.send(msgReturn("offMsg"))
        await bot.close()

        sys.exit(0)
    else:
        await ctx.send(msgReturn("notOwner"))

@slash.slash(name='update', description='Fixes me. Owner only', guild_ids=guild_ids)
async def update(ctx):
    if not isOwner(ctx):
        await ctx.send(msgReturn("notOwner"))
        return
    
    await ctx.send(msgReturn("offMsg"))
    os.system('sh update.sh &')

# for admins to admire shrek. Freezes the bot for a bit, so don't actually use
@slash.slash(name='shrek', description='WHAT ARE YOU DOING IN MY SWAMP. Owner only', guild_ids=guild_ids)
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
@slash.slash(name='courier',
    description='Sends a courier message to someone. Owner only',
    options=[
        create_option(
            name='user',
            description='Ping the person',
            option_type=6,
            required=True
        ),
        create_option(
            name='message',
            description='What do you want to send?',
            option_type=3,
            required=True
        )
    ],
    guild_ids=guild_ids
)
async def sendDM(ctx, user:discord.User=None, message:str=''):
    if not isOwner(ctx):
        await ctx.send(msgReturn("notOwner"))
        return

    452465370658373632
    await user.send(message)
        

# this allows the bot admins to change the status from the $help to something else
@slash.slash(name='status',
    description='Updates the bot\'s status. Owner only',
    options=[
        create_option(
            name='type',
            description='Type of status. Stream, help, music, or watching',
            option_type=3,
            required=True
        ),
        create_option(
            name='URL',
            description='Advanced presence URL',
            option_type=3,
            required=False
        )
    ],
    guild_ids=guild_ids
)
async def status(ctx, type:str='', URL:str=''):
    if not isOwner(ctx):
        await ctx.send(msgReturn('notOwner'))
        return

    if(type.lower() == 'stream'):
        await bot.change_presence(activity=discord.Streaming(name='Watching my creator', url=URL))
    elif(type.lower() == 'help'):
        await bot.change_presence(activity=discord.Game(name='with his food | /help'))
    elif(type.lower() == 'music'):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=URL))
    elif(type.lower() == 'watching'):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=URL))
        

# send you the servers the bot is in
@slash.slash(name='servers', description='Lists all joined servers. Owner only', guild_ids=guild_ids)
async def servers(ctx):
    #cheks if your owner
    if not isOwner(ctx):
        await ctx.send(msgReturn('notOwner'))
        return
    msg = ''
    #gets all the servers from bot object
    guilds = await bot.fetch_guilds(limit=150).flatten()
    msg = str(len(guilds)) + '\n'
    #loops through them and puts them in a string
    for i in guilds:
        msg += i.name + '\n'

    #creates a dm with user and dms it to them
    author = ctx.author
    await author.send(msg)
        

# command will change offten to test out commands
@bot.command()
async def test(ctx):
    if not isOwner(ctx): return
    print(ctx.message.content)
    await ctx.send(ctx.message.content)

# runs the bot after all the methods have been loaded to memory
bot.run(TOKEN)
