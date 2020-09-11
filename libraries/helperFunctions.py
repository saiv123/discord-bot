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
ownerId = [231957319737540608, 240636443829993473, 243774954955341828]

# used as a check for some command so only the people that are allowed to use it can use it
def isOwner(ctx):
    for i in ownerId:
        if(ctx.author.id == i):
            return True
    return False

class OwnersIgnoreCooldown(commands.Command):
    async def prepare(self, ctx):
        try:
            return await super().prepare(ctx)
        except commands.CommandOnCooldown as e:
            if isOwner(ctx.message.author.id):
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
    rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    print(rgb)
    return rgb
