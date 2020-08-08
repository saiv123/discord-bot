import requests 
from bs4 import BeautifulSoup

r = requests.get("https://www.twitch.tv/saiencevanadium")
soup = BeautifulSoup(r.content, "html.parser")
#print(r.content)
images = soup.findAll('img')
for image in images:
    #print image source
    print(image['src'])
    #print alternate text
    if 'alt' in image:
        print(image['alt'])