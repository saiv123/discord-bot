import discord
intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.members = True

import asyncio, discord
import time, datetime
import wolframalpha
from datetime import date
from datetime import datetime
from discord.ext import commands
from discord_slash import SlashCommand

from secret import TOKEN, id

# The guild ID of the test server. Remove when done testing
AUTORESPOND = True
# test_servers = [272155212347736065, 648012188685959169, 504049573694668801]

# setting up the bot, with its discritpion etc.
bot = commands.Bot(command_prefix='/', intents=intents)
slash = SlashCommand(bot, sync_commands=True)
ts = time.time()

# deleting default help comand
bot.remove_command('help')

client = wolframalpha.Client(id)

######################################
###Inizalization of bot DO NOT EDIT###
######################################

# Load all cogs
bot.load_extension("slash_commands.admin")
bot.load_extension("slash_commands.fun")
bot.load_extension("slash_commands.info")
bot.load_extension("slash_commands.math")
bot.load_extension("slash_commands.memes")
bot.load_extension("slash_commands.notes")
bot.load_extension("slash_commands.owner")
bot.load_extension("slash_commands.quotes")
bot.load_extension("slash_commands.rps")
bot.load_extension("slash_commands.move")

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
    tempD = datetime.today()
    tempDate = (tempD.day)
    tempMonth = (tempD.month)
    print("currDay: "+tempDate+"\ncurrMonth: "+tempMonth)
    user = bot.get_user(240636443829993473)

    if(tempDate == 7 and tempMonth == 12):
        age = tempD.year - 2000
        await user.send("Happy Birthday you are "+age, hidden=True)

    channel = message.channel

    if "456247671506599936" in message.content and message.author != bot.user:
        await channel.send("HEY! <@456247671506599936> YOUR MONTY FUCKING SUCKS <3~ ash aka motorcycle gal that loves ya")
    elif AUTORESPOND and "corn" in message.content.lower() and message.author != bot.user:
        await channel.send("https://cdn.discordapp.com/attachments/654783232969277453/738997605039603772/Corn_is_the_best_crop__wheat_is_worst.mp4")
    elif AUTORESPOND and "bird" in message.content.lower() and message.author != bot.user:
        await channel.send("The birds work for the bourgeoisie.")
    elif AUTORESPOND and " sai " in message.content.lower() and message.author != bot.user: #I solemnly swear that I am up to no good
        emoji = [':cowboy:',':shushing_face:']
        await message.add_reaction(emoji)
        await user.send(message.content)

    # Respond to last command
    await bot.process_commands(message)
bot.run(TOKEN)

# Currently does not work due to slash commands   :{
# useless with slash commands, but kept around in case we move back
# import traceback
# from libraries.prawn import getClosestFromList
# from Levenshtein import distance
# 
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

# runs the bot after all the methods have been loaded to memory