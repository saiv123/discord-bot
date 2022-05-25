import naff as dis

import time, datetime
import wolframalpha
from datetime import date
from datetime import datetime

import os

from secret import TOKEN, id

bot = dis.Client(sync_interactions=True)

ts = time.time()

client = wolframalpha.Client(id)

#black list lists  [sai's server, derp]
blackListServers = [648012188685959169, 531614305733574666]
#[finn, emilly, aqua, kyle]
blackListUsers = [361029057640529921, 705912686742863902, 361275648033030144, 288861358555136000]
#######################################
###Initialization of bot DO NOT EDIT###
#######################################

# Load all cogs
for root, dirs, files in os.walk("./scales"):
    for filename in files:
        if not filename.startswith("X-") and filename.endswith(".py"):
            command = root[2:].replace("/", ".") + "." + filename[:-3]  # gets cog path
            bot.mount_cog(command)

@dis.listen()
async def on_ready():
    print("user: " + bot.user.name)
    print("id: " + str(bot.user.id))
    # set the activity for the bot
    await bot.change_presence(status=dis.Status.ONLINE, activity=dis.Activity(type=dis.ActivityType.GAME, name="with his food | /help"))
    print("current time - " + str(ts))
    print("-----------")

@dis.listen(dis.events.PresenceUpdate)
async def streamCheck(event: dis.events.PresenceUpdate):
    if event.user.id == 240636443829993473:
        if event.activities[1] == dis.ActivityType.STREAMING:
            await bot.change_presence(status=dis.Status.ONLINE, activity=dis.Activity(type=dis.ActivityType.STREAMING, url=event.activities[2]))
        else:
            await bot.change_presence(status=dis.Status.ONLINE, activity=dis.Activity(type=dis.ActivityType.GAME, name="with his food | /help"))
    else:
        return

@dis.listen(dis.events.MemberAdd)
async def blackList(event: dis.events.MemberAdd):
    member = event.member
    if member.id in blackListUsers:
        user = await bot.fetch_user(240636443829993473)
        await user.send(f"ALERT - {member.nick} has joined the server {member.guild.name}!!!! 🚩")

        if member._guild_id in blackListServers:
            await member.send("You have been blacklisted from this server. Please contact the owner of this server, if you feel like this is a mistake.")
            await member.ban(reason="Blacklisted user")
            await user.send("Problem taken care of. :)")

@dis.listen(dis.events.MessageCreate)
async def on_message(event: dis.events.MessageCreate):
    message = event.message
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

###########
###TASKS###
###########

@dis.Task.create(dis.IntervalTrigger(days=1))
async def checkBrithday():
    tempD = datetime.today()
    tempDate = tempD.day
    tempMonth = tempD.month
    user = await bot.fetch_user(240636443829993473)

    if tempDate == 7 and tempMonth == 12:
        age = tempD.year - 2000
        await user.send("Happy Birthday you are "+str(age))

bot.start(TOKEN)