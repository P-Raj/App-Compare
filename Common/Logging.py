__author = "Pranav"
__email = "pranav09032@hotmail.com"

import sys
from datetime import datetime


class Logging:

	def __init__(self, logFilename):
		self.fileName = logFilename
		self.file = open(logFilename,'w')
		self.writeToFile = True

	def __init__(self):
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