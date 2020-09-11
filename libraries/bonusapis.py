import requests
import json, sys, os, string
import math
from imgutils import randomSaturatedColor

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

def getReqJSON(url, args={}):
    """Generic function to get json from an api request"""
    if url.endswith('/'):
        url = url[:-1]

    arg_str = ""
    if isinstance(args, dict):
        if len(args) > 0:
            arg_str = '?' + '&'.join([str(k)+'='+str(args[k]) for k in args])
    elif not isinstance(args, list):
        args = [str(args)]
    
    if len(args) > 0 and isinstance(args, list):
        arg_str = '/' + '/'.join(args)
    
    url = url + arg_str
    r = requests.get(url=url)
    try:
        return r.json()
    except:
        try:
            return json.loads(r.text+'}') # why not lul (some apis used here need it)
        except:
            return None

def advice(id:int=-1):
    """Gets an encouraging piece of advice"""
    if id >= 0:
        resp = getReqJSON('https://api.adviceslip.com/advice/', id)
    else:
        resp = getReqJSON('https://api.adviceslip.com/advice/')

    if 'slip' in resp and 'id' in resp['slip'] and 'advice' in resp['slip']:
        return {'author': 'Advice','id': resp['slip']['id'], 'quote': resp['slip']['advice']}
    return {}

def dumbTrumpQuote(tag:str=""):
    """Gets a stupid trump quote"""
    if len(tag) > 0:
        # Sadly, the api has no way to get a quote by a specific tag. Lets just scan 16 random quotes to try and get a matching tag
        # Returns a random quote otherwise
        foundQuote = dumbTrumpQuote()
        for i in range(15):
            if 'tag' in foundQuote and tag.lower() in foundQuote['tag'].lower():
                break
            foundQuote = dumbTrumpQuote()
        return foundQuote
    
    # Get quote json and parse to dict safely
    resp = getReqJSON('http://tronalddump.io/random/quote')
    parsed = {'author': 'Donald Trump'}
    if 'value' in resp:
        parsed['quote'] = resp['value']
    if 'appeared_at' in resp:
        parsed['date'] = str(resp['appeared_at']).replace('-',' ')[0:10]
    if 'tags' in resp and len(resp['tags']) > 0:
        parsed['tag'] = resp['tags'][0]
    if '_embedded' in resp and 'source' in resp['_embedded'] and len(resp['_embedded']['source']) > 0 and 'url' in resp['_embedded']['source'][0]:
        parsed['source'] = resp['_embedded']['source'][0]['url']
    return parsed


import nltk
from nltk.corpus import wordnet
nltk.download('vader_lexicon',quiet=True)
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

from itertools import product
def get_max_sim(list1, list2):
    allsyns1 = set(ss for word in list1 for ss in wordnet.synsets(word))
    allsyns2 = set(ss for word in list2 for ss in wordnet.synsets(word))
    best = max((wordnet.wup_similarity(s1, s2) or 0, s1, s2) for s1, s2 in product(allsyns1, allsyns2))
    return best

def get_sentiment(phrase:str, useAbs=True, weighted=False, average=True):
    words = phrase.split(' ')

    max_len = max(words, key=lambda s: len(s))
    total_score = 0.0
    for w in words:
        score = sid.polarity_scores(w)['compound']
        if useAbs:
            score = abs(score)
        if weighted:
            score *= 1-(len(w)/max_len)
        total_score += score

    if average:
        total_score /= len(words)
    return total_score

def get_contradiction_score(phrase1:str,phrase2:str):
    raw_score = 1/(abs(get_sentiment(phrase1,average=False)-get_sentiment(phrase2,average=False))+abs(phrase1.count('not')-phrase2.count('not'))/2.0)
    return round(4*math.log2(1+raw_score))/4 # Round to nearest 0.25 and use log2 to make spread smaller (might as well use a root)

def get_trump_contradiction(sameTag=False):
    q1 = dumbTrumpQuote()
    if not 'tag' in q1 or not 'quote' in q1:
        return
    
    if sameTag:
        q2 = dumbTrumpQuote(tag=q1['tag'])
    else:
        q2 = dumbTrumpQuote()
    
    if not 'quote' in q2:
        return
    return (get_contradiction_score(q1['quote'], q2['quote']), q1, q2)

def url_to_domain(url:str):
    if '//' in url:
        url = url[url.find('//')+2:]
    if '/' in url:
        url = url[:url.rfind('/')]
    if '.' in url:
        url = url[:url.rfind('.')]
    if len(url) >= 4 and url[3] == '.':
        url = url[4:]
    return url.strip().title()

def number_to_discord_emote(numb):
    numb = str(numb)
    numb.replace('10',':keycap_ten:')
    numb.replace('0',':zero:')
    numb.replace('1',':one:')
    numb.replace('2',':two:')
    numb.replace('3',':three:')
    numb.replace('4',':four:')
    numb.replace('5',':five:')
    numb.replace('6',':six:')
    numb.replace('7',':seven:')
    numb.replace('8',':eight:')
    numb.replace('9',':nine:')
    return numb

import discord
def quote_to_discord_embed(quote_dict:dict, switch=False):
    kwargs_dict = {'title': 'A quote','colour':randomSaturatedColor()}
    if 'quote' in quote_dict:
        kwargs_dict['description'] = quote_dict['quote']
    if 'author' in quote_dict:
        kwargs_dict['title'] = quote_dict['author']
    if 'source' in quote_dict:
        kwargs_dict['url'] = quote_dict['source']
        if 'author' in quote_dict:
            kwargs_dict['title'] = kwargs_dict['title'] + ' via '+url_to_domain(quote_dict['source'])
        else:
            kwargs_dict['title'] = 'via '+url_to_domain(quote_dict['source'])
    
    if switch:
        tempT = kwargs_dict['title']
        kwargs_dict['title'] = kwargs_dict['description']
        kwargs_dict['description'] = tempT
    
    embed=discord.Embed(**kwargs_dict)

    if 'date' in quote_dict:
        embed.set_footer(text=quote_dict['date'])
    return embed

def quote_to_discord_message(quote_dict:dict, include_source=False):
    if 'quote' not in quote_dict:
        return ''
    
    msg = '> ' + str(quote_dict['quote']).replace('\n', '\n> ')
    msg = msg+'\n'
    if 'author' in quote_dict:
        msg = msg + '~'+quote_dict['author']
    if 'date' in quote_dict:
        msg = msg+' ('+quote_dict['date']+')'
    if 'source' in quote_dict and include_source:
        msg = msg+'\nFrom: '+quote_dict['source']
    return msg

import re
def getColor(entry:str, code=''):
    entry = re.sub(r"(\s*[:punct:]+\s*)|(\s+)", ',', entry.strip())
    
    # if type is not given, attempt auto detection
    if len(code) <= 1:
        if '#' in entry or ',' not in entry:
            entry = entry.replace(',','').replace('#','')
            code = 'hex'
        elif entry.count(',') == 2: # assume rgb
            code = 'rgb'
        elif entry.count(',') == 3: # assume cmyk
            code = 'cmyk'

    # get and parse response
    resp = getReqJSON('https://www.thecolorapi.com/id?format=json&'+str(code)+'='+str(entry))
    if str(resp).count('None')  > 2: raise ValueError

    color_dict = {'url': 'https://www.thecolorapi.com/id?format=html&'+str(code)+'='+str(entry)}
    if 'hex' in resp: color_dict['hex'] = resp['hex']['clean']
    if 'rgb' in resp: color_dict['rgb'] = [resp['rgb']['r'],resp['rgb']['g'],resp['rgb']['b']]
    if 'hsl' in resp: color_dict['hsl'] = [resp['hsl']['h'],resp['hsl']['s'],resp['hsl']['l']]
    if 'hsv' in resp: color_dict['hsv'] = [resp['hsv']['h'],resp['hsv']['s'],resp['hsv']['v']]
    if 'XYZ' in resp: color_dict['xyz'] = [resp['XYZ']['X'],resp['XYZ']['Y'],resp['XYZ']['Z']]
    if 'cmyk' in resp: color_dict['cmyk'] = [resp['cmyk']['c'],resp['cmyk']['m'],resp['cmyk']['y'],resp['cmyk']['k']]

    if 'image' in resp and 'named' in resp['image']: color_dict['img'] = resp['image']['named']
    if 'name' in resp:
        if 'value' in resp['name']: color_dict['name'] = resp['name']['value']
        if 'distance' in resp['name']: color_dict['distance'] = resp['name']['distance']
    
    return color_dict

def colorDictToEmbed(color_dict, titled=True, named=True):
    kwargs_dict = {'title':'Color','color':randomSaturatedColor()}
    if 'hex' in color_dict: kwargs_dict['color'] = int(color_dict['hex'], 16)
    if 'name' in color_dict and titled: kwargs_dict['title'] = color_dict['name']

    embed = discord.Embed(**kwargs_dict)
    embed.add_field(name='Hex',value='#'+str(color_dict['hex']), inline=True)
    
    # add alternate values
    vals_to_add = ('rgb','hsl','hsv','cmyk')
    for val in vals_to_add:
        if val in color_dict: embed.add_field(name=val.upper(),value='({})'.format(', '.join([str(i) for i in color_dict[val]])), inline=True)
    
    # add image
    url_add = '&named=False' if not named else ''
    if 'img' in color_dict: embed.set_image(url=color_dict['img']+url_add)

    return embed
if __name__ == "__main__":
    # print('Advice:\n'+str(advice()))
    # print('Stupid Trump Quote:\n'+str(dumbTrumpQuote()))
    # print('Stupid Trump Quote on Hillary:\n'+str(dumbTrumpQuote(tag='Hillary')))
    # print(get_trump_contradiction())
    print(getColor('255 5 5'))
    print(colorDictToEmbed(getColor('255 5 5')))
