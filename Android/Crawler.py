import DataLink as DL
import urllib
from bs4 import BeautifulSoup
import os
import re
from Manager import FileManager

Handler = FileManager.Handler

class AndroidMarket(Handler, object):

    
    def __init__(self, url):
        super(AndroidMarket, self).__init__(url)

    def startDownload(self):

            if not self.parser:
                return

            for elem in self.parser.find('div', {'class': 'card-list'}).find_all('div'):
                elemInfo = {}
                for item in elem.find_all('div'):
                    print item['class'], self.cleanString(item.text)
                    # HAVE NOT HANDLED RATING
            

if __name__ == "__main__":
    for url in DL.generateURL():
        A = AndroidMarket(url)
        A.startDownload()
        break
