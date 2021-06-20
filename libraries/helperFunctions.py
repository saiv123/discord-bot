import sys, os
FILEPATH, filename = os.path.split(os.path.abspath(__file__))
sys.path.insert(1, FILEPATH)

import asyncio, discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import prawn, imgutils
import json, random
##########################
###bots helper commands###
##########################

# List of Owners/Bot admins
ownerId = [231957319737540608, 240636443829993473, 299231063098654720]

#list of secure servers
servers = [648012188685959169, 749047084275204166, 297919267620388864]

#checking for server for sad command
def checkAuthSerers(ctx):
    for i in servers:
        if ctx.message.guild.id == i:
            return True
    return False

# used as a check for some command so only the people that are allowed to use it can use it
def isOwner(ctx):
    authid = ctx.id if isinstance(ctx, discord.User) else ctx.author.id
    for id in ownerId:
        if(authid == id):
            return True
    return False

class OwnersIgnoreCooldown(commands.Command):
    async def prepare(self, ctx):
        try:
            return await super().prepare(ctx)
        except commands.CommandOnCooldown as e:
            if isOwner(ctx):
                return
            else:
                raise e

# gets a message from the dictionary with the type inputed
def msgReturn(type):
    data = json.load(open("msg.json"))
    typeM = data[type]
    msgData = random.choice(typeM)
    del data, typeM
    return msgData

# Splits a string into several sub-2000 char strings
def splitLongStrings(str, chars=1500, preferred_char=' '):
    messages = []
    if preferred_char not in str:  # If there are no spaces, don't respect spaces
        message = ""
        for c in str:
            if len(message) >= chars:  # >= is equivalent to adding 1 to len(message)
                messages.append(message)
                message = ""
            message = message + c
        messages.append(message)
        return messages
    # If there are spaces, respect them
    words = str.split(preferred_char)
    message = ""
    for word in words:
        if len(message) + len(word) > chars:
            messages.append(message[1:])  # delete leading space
            message = ""
        message = message + preferred_char + word
    if len(message) > 1:
        messages.append(message[1:])
    return messages

def gen_invis(i:int=1):
    if i < 0: i = 0
    return str(chr(0xffa0)) * (i+1) + ' ' + str(chr(0x1cbc)) * 4

# split a string or a list of strings into subfields of an embed
def add_to_embed(embed:discord.Embed or str or None, message:str or list, chars:int=1000, use_description:bool=True):
    if embed == None:
        embed = discord.Embed(title=chr(0xffa0))
        embed.color = discord.Colour(imgutils.randomSaturatedColor())
    elif isinstance(embed, str):
        embed = discord.Embed(title=embed)
        embed.color = discord.Colour(imgutils.randomSaturatedColor())
    assert isinstance(embed, discord.Embed), 'add_to_embed embed input not parseable to discord.Embed'

    if chars > 2000: chars = 2000

    current_fields = '\n'.join([x.value for x in embed.fields])
    if isinstance(message, list): message = '\n'.join(message)
    message = f'{current_fields}\n{message}'

    dummy_embed = discord.Embed(title=chr(0xffa0))
    dummy_embed.color = discord.Colour(imgutils.randomSaturatedColor())
    try: dummy_embed.author = embed.author
    except: pass
    try: dummy_embed.footer = embed.footer
    except: pass
    try: dummy_embed.provider = embed.provider
    except: pass

    # each embed can hold 6000 chars
    message = splitLongStrings(message, chars=5000, preferred_char='\n')

    embeds = [embed] + [dummy_embed.copy() for x in range(len(message)-1)]
    for i in range(len(message)):
        msg_txt = splitLongStrings(message[i], chars=chars, preferred_char='\n' if message[i].count('\n') >= len(message[i])/(1.5*chars) else ' ')
        if use_description: embeds[i].description = f'{embeds[i].description}\n{msg_txt.pop(0)}' if len(embeds[i].description) else msg_txt.pop(0)
        for j in range(len(msg_txt)):
            embeds[i].add_field(name=gen_invis(i=j), value=msg_txt[j], inline=False)
    return embeds

# Gets embed responses from a library of links
def getEmbedsFromLibraryQuery(libraryPath, query):
    # If query is categories, get categories
    if 'category' in query.lower() or 'categories' in query.lower():
        color = imgutils.randomSaturatedColor()
        embeds = []
        for message in splitLongStrings(', '.join(map(prawn.getFileName,prawn.getFileList(libraryPath)))):
            embeds.append(discord.Embed(description=message, color=color))
        return embeds
    # Otherwise, get image from query
    namedImg = ('Error', 'https://www.prajwaldesai.com/wp-content/uploads/2014/01/error-code.jpeg')

    # Iterate up to 5x to try and get a valid image
    for i in range(5):
        if len(str(query)) <= 2:
            namedImg = prawn.getRandom(path=libraryPath)
        else:
            namedImg = prawn.getRandomLineFromQuery(query, path=libraryPath)
        if imgutils.isUrlValidImage(namedImg[1]):
            break

    if not imgutils.isUrlValidImage(namedImg[1]):  # Print error
        print('Image not valid at ' +namedImg[1] + '\n\t(name ' + namedImg[0] + ')')

    embed = discord.Embed(description=namedImg[0], color=imgutils.getAverageColor(namedImg[1]))
    embed.set_image(url=namedImg[1])
    return [embed]

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

def RgbToHex(red, green, blue):
    hex = '#%02x%02x%02x' % (red, green, blue)
    print(hex)
    return hex
def HexToRgb(hex):
    hex=hex.lstrip('#')
    rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4)) #using tuple object to split the string to convert to rgb
    print(rgb)
    return rgb
