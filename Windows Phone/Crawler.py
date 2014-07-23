__author__ = "Pranav Raj"
__email__ = "pranav09032@hotmail.com"

import os
import re
import urllib
from bs4 import BeautifulSoup
from Manager import FileManager

Handler = FileManager.Handler

class Items(Handler, object):

    def __init__(self, url, category):
        super(Items, self).__init__(url)
        self.category = category
        self.updateName(category)
        self.items = []

    def extractContents(self):
        self.parser = self.getParser()
        contents = self.getIterator(("ul", {"class": "galerie"}),
                                    ('li',{}))
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
