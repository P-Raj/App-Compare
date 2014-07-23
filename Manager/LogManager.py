__author = "Pranav"
__email = "pranav09032@hotmail.com"

import sys
from datetime import datetime


class Handler:

    def __init__(self, logFilename = None):
        if logFilename:
            self.fileName = logFilename
            self.file = open(logFilename,'w')
            self.writeToFile = True
        else:
            self.file = sys.stdout
            self.writeToFile = False

    def cleanLog(self):
        if self.writeToFile:
            self.file = open(self.fileName, 'w')
            self.file.truncate()

    def _getTime(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def log(self, text):
        logTime = self._getTime()
        self.file.write(logTime + "\t"
                        + text)