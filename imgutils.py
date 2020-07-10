from io import BytesIO

import requests
from PIL import Image

import random

def isImage(image_urls):
    resp = requests.get(image_urls)
    return resp.ok

def getAverageColor(image_url):
    # get image from web
    resp = requests.get(image_url)
    if not resp.ok: # if not valid, return random saturated color
        return randomSaturatedColor()
    img = Image.open(BytesIO(resp.content))

    # squeeze the image into 1 pixel
    img2 = img.resize((1, 1))

    color = img2.getpixel((0, 0))
    #converts the 3 rgb values into a hex value
    hex = '{:02x}{:02x}{:02x}'.format(*color)
    return int(hex.upper(), 16) #convert the hex string to an int

def randomSaturatedColor(minSat=64,steps=1):
    if minSat <= 1:
        minSat = minSat*255
    minSat = min(minSat, 255) #must be lower than 255

    hex = '{:02x}{:02x}{:02x}'.format(random.randrange(minSat, 255, steps),random.randrange(minSat, 255, steps),random.randrange(minSat, 255, steps))
    return int(hex.upper(), 16)

if __name__ == '__main__':
    for i in range(5):
        print(getAverageColor('https://i.redd.it/v7epwhtv4w551.jpg'))
        print(getAverageColor('https://i.imgur.com/vtHTdK4.jpg'))
    print(randomSaturatedColor())
