##########################
###bots helper commands###
##########################

# used as a check for some command so only the people that are allowed to use it can use it
def isOwner(ctx):
    for i in ownerId:
        if(ctx.author.id == i):
            return True
    return False

# gets a message from the dictionary with the type inputed
def msgReturn(type):
    data = json.load(open("msg.json"))
    typeM = data[type]
    msgData = random.choice(typeM)
    del data, typeM
    return msgData

# Splits a string into several sub-2000 char strings
def splitLongStrings(str, chars=1500):
    messages = []
    if ' ' not in str:  # If there are no spaces, don't respect spaces
        message = ""
        for c in str:
            if len(message) >= chars:  # >= is equivalent to adding 1 to len(message)
                messages.append(message)
                message = ""
            message = message + c
        messages.append(message)
        return messages
    # If there are spaces, respect them
    words = str.split(' ')
    message = ""
    for word in words:
        if len(message) + len(word) > chars:
            messages.append(message[1:])  # delete leading space
            message = ""
        message = message + ' ' + word
    if len(message) > 1:
        messages.append(message[1:])
    return messages

# Gets embed responses from a library of links
def getEmbedsFromLibraryQuery(libraryPath, query):
    # If query is categories, get categories
    if 'category' in query.lower() or 'categories' in query.lower():
        color = imgutils.randomSaturatedColor()
        embeds = []
        for message in splitLongStrings(' '.join(prawn.getCategoryMessages(path=libraryPath))):
            embeds.append(discord.Embed(description=message, color=color))
        return embeds
    # Otherwise, get image from query
    namedImg = (
        'Error', 'https://www.prajwaldesai.com/wp-content/uploads/2014/01/error-code.jpeg')

    # Iterate up to 5x to try and get a valid image
    for i in range(5):
        if len(str(query)) <= 2:
            namedImg = prawn.getRandom(path=libraryPath)
        else:
            namedImg = prawn.getRandomLineFromQuery(query, path=libraryPath)
        if imgutils.isUrlValidImage(namedImg[1]):
            break
    if not imgutils.isUrlValidImage(namedImg[1]):  # Print error
        print('Image not valid at ' +
              namedImg[1] + '\n\t(name ' + namedImg[0] + ')')

    embed = discord.Embed(description=namedImg[0], color=imgutils.getAverageColor(
        namedImg[1]))  # 16777... is just FFFFFF in base10
    embed.set_image(url=namedImg[1])
    return [embed]
