__author__ = "Pranav Raj"
__email__ = "pranav09032@hotmail.com"

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
        string = string.encode('ascii','ignore')
        string = string.strip()
        string = re.sub(' +', ' ', string)
        return string

    def getTitle(self):
        return "".join(char
                       for char in self.cleanString(self.parser.title.string)
                       if char.isalnum() or char == " ")

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


class Items(Handler, object):

    def __init__(self, url, category):

        super(Items, self).__init__(url)
        self.category = category
        self.updateName(category)
        self.items = []

    def extractContents(self):
        self.parser = self.getParser()
        contents = self.parser.find("ul", {"class": "galerie"}).find_all('li')
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

        def gettext(obj, key='content'):
            objL = {}
            try:
                objL['content'] = obj[key]
            except:
                pass
            try:
                objL['text'] = obj.text
            except:
                pass
            return objL

        rating = self.parser.find('p',
                                  {
                                  'class': 'flviewinfos'
                                  })
        self.contents['rating'] =
        {
            'content': rating.find('span').text,
            'text': rating.find('span').text
        }
        self.contents['published'] = gettext(self.parser.find('p',
                                             {
                                             'class': 'flviewinfos'
                                             }))
        self.contents['publisher'] = gettext(self.parser.find('p',
                                             {
                                             'class': 'flviewinfos'
                                             }).find('a'),
                                             'href')
        self.contents['version'] = gettext(self.parser.find('p',
                                           {
                                           'class': 'flviewinfos'
                                           }))
        self.contents['size'] = gettext(self.parser.find('p',
                                        {
                                        'class': 'flviewinfos'
                                        }))
        self.contents['operating system'] = gettext(self.parser.find('p',
                                                    {
                                                    'class': 'flviewinfos'
                                                    }))

        print self.contents

    def write(self):
        with open(self.getFilePath() + ".property", 'w') as fp:
            for meta in self.metaData:
                fp.write(self.cleanString(meta) + "\n")
            for key in self.contents:
                fp.write(key + ":" + "\n")
                fp.write("\t" + "content" + ":" +
                         self.cleanString(
                            self.contents[key].get('content', "None")
                         + "\n")
                fp.write("\t" + "text" + ":" +
                         self.cleanString(
                            self.contents[key].get('text', "None")
                         + "\n")

url = "http://windowsphoneapplist.com/en/\windowsphone.booksandreference/downloadRank/"
items = Items(url, "books")
items.downloadContents()
