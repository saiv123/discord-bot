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
AUTORESPOND = True
test_servers = [272155212347736065, 648012188685959169, 504049573694668801]

# setting up the bot, with its discritpion etc.
bot = commands.Bot(command_prefix='/', intents=intents)
slash = SlashCommand(bot, sync_commands=True)
ts = time.time()

# setting up LyricGenius stuff
Gen = LyrGen.Genius(GenID)

# deleting default help comand
bot.remove_command('help')

######################################
###Inizalization of bot DO NOT EDIT###
######################################

# Load all cogs
bot.load_extension("slash_commands.info")
bot.load_extension("slash_commands.notes")
bot.load_extension("slash_commands.songs")
bot.load_extension("slash_commands.shouldI")
bot.load_extension("slash_commands.math")
bot.load_extension("slash_commands.quotes")
bot.load_extension("slash_commands.admin")
# bot.load_extension("slash_commands.shouldI")
# bot.load_extension("slash_commands.shouldI")
# bot.load_extension("slash_commands.shouldI")
# bot.load_extension("slash_commands.shouldI")
# bot.load_extension("slash_commands.shouldI")
# bot.load_extension("slash_commands.shouldI")


#what the bot does on boot
@bot.event
async def on_ready():
    print('user: ' + bot.user.name)
    print('id: ' + str(bot.user.id))
    # setst the activity for the bot
    await bot.change_presence(activity=discord.Game(name='with his food | /help'))
    print('current time - ' + str(ts))
    print('-----------')

#Changes the bots status to my stream when Sai streams
@bot.event
async def on_member_update(before, after):
    #check if the users update is sai
    if(before.id == 240636443829993473):
        currActicity = after.activities
        #for activities that are more than 2 this for loop will fix a index out of range error it by looping through the tupple
        for i in range(len(currActicity)):
            if(after.activities[i].type is discord.ActivityType.streaming):
                await bot.change_presence(activity=discord.Streaming(name="Streaming"+after.activities[i].game+"!", url=after.activities[i].url))
            else:
                await bot.change_presence(activity=discord.Game(name='with his food | /help'))

# for every message it does these checks
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
# useless with slash commands, but kept around in case we move back
# @bot.event
# async def on_command_error(ctx, error):
#     msgSend = "An internal error has occured. Use /contact to contact the owner if it persists"
#     if isinstance(error, commands.MissingRequiredArgument):
#         e_msg = ', a '.join(str(error.param).replace('params','').split(':'))
#         msgSend = f'You did not use the command correctly\nYou\'re missing {e_msg}\n\nIf you don\'t know how to use the command, use the /help command to see how to use all commands.'
#     elif isinstance(error, commands.BadArgument):
#         e_msg = ' and '.join(error.args)
#         msgSend = f'You did not use the command correctly\nYou\'re arguements are wrong: {e_msg}\n\nIf you don\'t know how to use the command, use the /help command to see how to use all commands.'
#     elif isinstance(error, commands.CommandOnCooldown):
#         msgSend = 'You\'re on cooldown for '+ctx.invoked_with + '.\nPlease wait another '+str(round(error.retry_after))+' seconds'
#     elif isinstance(error, commands.CommandNotFound): 
#         cmd = str(ctx.invoked_with)
#         cmd_list = [cmd.name for cmd in bot.commands]
#         mlo = getClosestFromList(cmd_list, cmd)
#         if distance(cmd, mlo) <= 0.6*len(cmd):
#             msgSend= f"Sorry, but that is not a valid command. Did you mean {mlo}?\n\nYou can add suggestions at [suggestions Website](https://github.com/saiv123/discord-bot/issues/new/choose)"
#         else:
#             msgSend = "Sorry but that is not a valid command\nYou can add suggestions at [suggestions Website](https://github.com/saiv123/discord-bot/issues/new/choose)"

#     embeds = add_to_embed('Error','Command Entered: {}\n{}'.format(ctx.message.content, msgSend))
#     for embed in embeds:
#         embed.set_footer(text='Command Broken by: ' + ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
#         await ctx.send(embed=embed)
#     print(error)
#     print(traceback.format_exc()) # Attempt to print exception

##############
###Commands###
##############

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

@slash.slash(name='ping', description='What\'s my speed?' )
async def ping(ctx):
    await ctx.respond()

    embed = add_to_embed('Ping','Latency: {0}ms'.format(round(bot.latency*1000, 1)))[0]
    embed.set_footer(text='Ping Measured by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

    #t = (msg.created_at - ctx.created_at).total_seconds() * 1000
    #embed = add_to_embed('Ping','Latency: {}ms\nRound Trip Time: {}ms'.format(round(bot.latency*1000, 1), round(t, 1)))[0]
    #embed.set_footer(text='Ping Measured by: ' + ctx.author.name, icon_url=ctx.author.avatar_url)
    #await msg.edit(content=None, embed=embed)

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

)
async def roll(ctx, dice:str='1d6'):
    if isOwner(ctx): ctx.defer() # I solemnly swear that I am up to no good

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

        if isOwner(ctx) or (0 < rolls <= MAXROLLS and 1 < sides <= MAXSIDES):
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

################################
###Commands to make you unsad###
################################

#up date to how the command will work, it will be limited to onnce ever 24 hours, but will always send the quote even if it does join the vc
#play / do something depending on if the user is in a voice channel or not
@slash.slash(name='sad', description='Makes you unsad' )
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

# runs the bot after all the methods have been loaded to memory
bot.run(TOKEN)