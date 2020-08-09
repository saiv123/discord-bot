import requests
import json
import random


def getQuoteApi():
    url = "https://quotes15.p.rapidapi.com/quotes/random/"

    querystring = {"language_code": "en"}

    headers = {
        'x-rapidapi-host': "quotes15.p.rapidapi.com",
        'x-rapidapi-key': "5046ada3a3msh209ead9f0d8e14bp12071ajsna1080969f1cc"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    quote = json.loads(response.text)
    qText = quote["content"]
    aText = quote["originator"]["name"]

    return {'quote':qText,'author':aText}


def getQuoteJSON():
    quote = 'Tough times dont last, but tough people do'
    with open('\libraries\quotes.txt', mode='r') as file:
        l = file.read().split('\n')
        quote = random.choice(l)
        while len(quote) < 2:  # Just make sure we don't get a blank line
            quote = random.choice(l)
    return {'quote': quote}
