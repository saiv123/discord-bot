import os
import random

from Levenshtein import distance

prawnPath = 'MyHomework/'


def getFileList(path):
    filelist = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if str(file).endswith('.txt'):
                filelist.append(file)
    return filelist


def getClosestFromList(list, query):
    minDist = 10000000  # 9223372036854775807
    minValue = None if len(list) <= 0 else list[0]
    for i in list:
        dist = distance(str(query), str(i))
        if dist < minDist:
            minDist = dist
            minValue = i
    return minValue

# Will infinite-loop if a file is only a single blank line


def getRandomLineFromFile(path):
    line = ''
    with open(path, mode='r') as file:
        l = file.readlines()
        line = random.choice(l)
        # Just make sure we don't get a blank line
        while not line or not line.replace('\n', ''):
            line = random.choice(l)
    return line.replace('\n', '')


def getFileName(filePath):
    if '.' in filePath:
        filePath = filePath[:filePath.rfind('.')]
    if '/' in filePath:
        filePath = filePath[filePath.rfind('/') + 1:]
    if '\\' in filePath:
        filePath = filePath[filePath.rfind('\\') + 1:]
    return filePath.replace('_', ' ').replace('urls', '').replace('url', '')


def getRandom(path=prawnPath):
    filePath = random.choice(getFileList(path))
    return 'From ' + getFileName(filePath), getRandomLineFromFile(path + filePath)


def getRandomLineFromQuery(query, path=prawnPath):
    closest = getClosestFromList(getFileList(path), query)
    modifier = ''

    # Let's check for a threshold
    dist = distance(getFileName(closest).lower(), query.lower())
    if dist > (len(closest) - 3) * 0.4:  # Can be 40% wrong
        #categories = ', '.join(map(getFileName, getFileList(path)))
        return 'Error, category not found.\nYou should use the argument \'category\' to list categories. \nDid you mean ' + getFileName(closest) + '?', ''

    # If 20% wrong, hassle them
    if dist > (len(closest) - 3) * 0.2:  # Can be 40% wrong
        modifier = 'Using category ```' + getFileName(closest) + '```\n'

    # Threshold is met, return random line from file
    return modifier, getRandomLineFromFile(path + closest)

# Unused, returns a list of lists where each element contains up to 30 file names, separated by commas
def getCategoryMessages(path=prawnPath):
    messageList = []
    fileList = getFileList(path)

    i = 0
    subList = []
    while i < len(fileList):
        subList.append(fileList[i])
        if i % 30 == 0:
            messageList.append(', '.join(map(getFileName, subList)))
            subList.clear()
        i += 1
    messageList.append(', '.join(map(getFileName, subList)))
    return messageList
