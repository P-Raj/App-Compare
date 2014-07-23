__author__ = "Pranav Raj"
__email__ = "pranav09032@hotmail.com"

import os
import re
import urllib
from bs4 import BeautifulSoup
from Manager import FileManager
import DataLink as DL

Handler = FileManager.Handler

class Items(Handler, object):

    def __init__(self, url, category):

        super(Items, self).__init__(url)
        self.category = category
        self.updateName(category)
        self.items = []
        self.maxPagesParsed = 100

    def extractContents(self):
        self.parser = self.getParser()
        contents = []
        
        for char in list(map(chr, range(65, 91))):
            for count in range(100):
                
            
            self.parser.find("ul", {"class": "galerie"}).find_all('li')
        return contents

    def parseMetaData(self, header):
        metaData = header.find_all('dl')
        imageLink = metaData[0].find('img')['src'].strip()
        metaData = [imageLink] + [self.cleanString(meta)
                                  for meta in metaData[1:]]
        return metaData

    def downloadContents(self):
        for content in self.extractContents():
            for elements in content.find_all('a'):
                url = elements['href']
                metaData = self.parseMetaData(elements)
                self.items.append(Item(url, metaData))


class Item(Handler):

    def __init__(self, url, metaData):

        self.url = url
        self.metaData = metaData
        super(Item, self).__init__(url)
        self.contents = {}
        self.extractContents()
        self.write()

    def extractContents(self):
        self.contents = {}

        
        
        