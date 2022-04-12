import discord

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.members = True
intents.voice_states = True

import asyncio
import time, datetime
import wolframalpha
from datetime import date
from datetime import datetime
from discord.ext import commands
from discord_slash import SlashCommand

import os

from secret import TOKEN, id

# The guild ID of the test server. Remove when done testing
AUTORESPOND = True
# test_servers = [272155212347736065, 648012188685959169, 504049573694668801]

# setting up the bot, with its discritpion etc.
bot = commands.Bot(command_prefix="/", intents=intents)
slash = SlashCommand(bot, sync_commands=True)
ts = time.time()

# deleting default help comand
bot.remove_command("help")

client = wolframalpha.Client(id)


#black list lists  [sai's server, derp]
blackListServers = [648012188685959169, 531614305733574666]
#[finn, emilly, aqua, kyle]
blackListUsers = [361029057640529921, 705912686742863902, 361275648033030144, 288861358555136000]
#######################################
###Initialization of bot DO NOT EDIT###
#######################################

# Load all cogs
for root, dirs, files in os.walk("./slash_commands"):
    for filename in files:
        if not filename.startswith("X-") and filename.endswith(".py"):
            command = root[2:].replace("/", ".") + "." + filename[:-3]  # gets cog path
            bot.load_extension(command)

# what the bot does on boot
@bot.event
async def on_ready():
    print("user: " + bot.user.name)
    print("id: " + str(bot.user.id))
    # set the activity for the bot
    await bot.change_presence(activity=discord.Game(name="with his food | /help"))
    print("current time - " + str(ts))
    print("-----------")


# Changes the bots status to my stream when Sai streams
@bot.event
async def on_member_update(before, after):
    # check if the users update is sai
    if before.id == 240636443829993473:
        currActicity = after.activities
        # for activities that are more than 2 this for loop will fix a index out of range error it by looping through the tupple
        for i in range(len(currActicity)):
            if after.activities[i].type is discord.ActivityType.streaming:
                await bot.change_presence(
                    activity=discord.Streaming(
                        name="Streaming" + after.activities[i].game + "!",
                        url=after.activities[i].url,
                    )
                )
            else:
                await bot.change_presence(
                    activity=discord.Game(name="with his food | /help")
                )
    else:
        return

@bot.event
@commands.bot_has_permissions(administrator=True)
async def on_member_join(member):
    if member.id in blackListUsers:
        user = bot.get_user(240636443829993473)
        await user.send(f"ALERT - {member.name} has joined the server {member.guild.name}!!!! 🚩")

        if member.guild.id in blackListServers:
            await member.send("You have been blacklisted from this server. Please contact the owner of this server, if you feel like this is a mistake.")
            await member.ban(reason="Blacklisted user")
            await user.send("Problem taken care of. :)")


# for every message it does these checks
@bot.event
async def on_message(message):
    channel = message.channel
    tempD = datetime.today()
    tempDate = tempD.day
    tempMonth = tempD.month
    user = bot.get_user(240636443829993473)

    if tempDate == 7 and tempMonth == 12:
        age = tempD.year - 2000
        await user.send("Happy Birthday you are "+str(age))

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
    # Respond to last command
    await bot.process_commands(message)

bot.run(TOKEN)

# Currently does not work due to slash commands   :{
# useless with slash commands, but kept around in case we move back
import traceback
from libraries.prawn import getClosestFromList
from Levenshtein import distance

@bot.event
async def on_slash_command_error(ctx, error):
    msgSend = "An internal error has occurred. Use /contact to contact the owner if it persists"
    if isinstance(error, commands.MissingRequiredArgument):
        e_msg = ", a ".join(str(error.param).replace("params", "").split(":"))
        msgSend = f"You did not use the command correctly\nYou're missing {e_msg}\n\nIf you don't know how to use the command, use the /help command to see how to use all commands."
    elif isinstance(error, commands.BadArgument):
        e_msg = " and ".join(error.args)
        msgSend = f"You did not use the command correctly\nYou're arguments are wrong: {e_msg}\n\nIf you don't know how to use the command, use the /help command to see how to use all commands."
    elif isinstance(error, commands.CommandOnCooldown):
        msgSend = (
            "You're on cooldown for "
            + ctx.invoked_with
            + ".\nPlease wait another "
            + str(round(error.retry_after))
            + " seconds"
        )
    elif isinstance(error, commands.CommandNotFound):
        cmd = str(ctx.invoked_with)
        cmd_list = [cmd.name for cmd in bot.commands]
        mlo = getClosestFromList(cmd_list, cmd)
        if distance(cmd, mlo) <= 0.6 * len(cmd):
            msgSend = f"Sorry, but that is not a valid command. Did you mean {mlo}?\n\nYou can add suggestions at [suggestions Website](https://github.com/saiv123/discord-bot/issues/new/choose)"
        else:
            msgSend = "Sorry but that is not a valid command\nYou can add suggestions at [suggestions Website](https://github.com/saiv123/discord-bot/issues/new/choose)"

    embeds = add_to_embed(
        "Error", "Command Entered: {}\n{}".format(ctx.message.content, msgSend)
    )
    for embed in embeds:
        embed.set_footer(
            text="Command Broken by: " + ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url,
        )
        await ctx.send(embed=embed)
    print(error)
    print("----------------> " + ctx.guild.name)
    print(traceback.format_exc())  # Attempt to print exception
