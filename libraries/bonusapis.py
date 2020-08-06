import requests
import json


#r = requests.get(url='https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
#print(r.json())

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
        return {'id': resp['slip']['id'], 'quote': resp['slip']['advice']}
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
    parsed = dict()
    if 'value' in resp:
        parsed['quote'] = resp['value']
    if 'appeared_at' in resp:
        parsed['date'] = str(resp['appeared_at']).replace('-',' ')[0:10]
    if 'tags' in resp and len(resp['tags']) > 0:
        parsed['tag'] = resp['tags'][0]
    if '_embedded' in resp and 'source' in resp['_embedded'] and len(resp['_embedded']['source']) > 0 and 'url' in resp['_embedded']['source'][0]:
        parsed['source'] = resp['_embedded']['source'][0]['url']
    return parsed

if __name__ == "__main__":
    print('Advice:\n'+str(advice()))
    print('Stupid Trump Quote:\n'+str(dumbTrumpQuote()))
    print('Stupid Trump Quote on Hillary:\n'+str(dumbTrumpQuote(tag='Hillary')))
