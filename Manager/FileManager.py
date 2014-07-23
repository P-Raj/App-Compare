import os
import re
import urllib
from bs4 import BeautifulSoup

class Handler:

    def __init__(self, url):
        self.url = url
        self.property = {}
        self.homeDir = os.path.dirname(__file__)
        self.parser = self.getParser()
        self.name = self.getTitle()
        self.setupFolder()

    def updateName(self, name):
        self.name = name

    def setupFolder(self):
        dataDir = os.path.join(self.homeDir, self.name)
        if not os.path.exists(dataDir):
            os.makedirs(dataDir)
        os.chdir(dataDir)

    def cleanString(self, string):
        string = string.encode('ascii', 'ignore')
        string = string.strip()
        string = re.sub(' +', ' ', string)
        return string

    def getTitle(self):
        return "".join(char
                       for char in self.cleanString(self.parser.title.string)
                       if char.isalnum() or char == " ")
        
    def getIterator(self, headInfo, iteratorInfo):
        iterator = self.parser.find(*headInfo).findAll(*iteratorInfo)
        return iterator

    def getFilePath(self):
        return os.path.join(self.homeDir, self.name)

    def getRequest(self, url):
        return urllib.urlopen(url).read()

    def getParser(self):
        parser = BeautifulSoup(self.getRequest(self.url))
        return parser

    def saveProperty(self, key, value):
        self.property[key] = value

    def writeProperty(self):
        fileName = self.getTitle() + ".property"
        with open(fileName, 'w') as f:
            f.write("\n".join(
                key + ":" + self.property[key]
                for key in self.property))
