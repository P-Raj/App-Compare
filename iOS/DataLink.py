import urllib
from bs4 import BeautifulSoup

BASE_URL = "https://itunes.apple.com/in/genre/ios/id36"

def getParser(url):
    bs = BeautifulSoup(urllib.urlopen(url).read())
    return bs

def getIterator(parser, headInfo, iteratorInfo):
    iterator = parser.find(*headInfo).findAll(*iteratorInfo)
    return iterator

def getCategories():
    parser = getParser(BASE_URL)
    for item in getIterator(parser,
                            ('div',{'class':'grid3-column'}),
                            ('li',{})):
        link = item.find('a')
        yield link.text, link['href']
        
for i in getCategories():
    print i
        
    
    