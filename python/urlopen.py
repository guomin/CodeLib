#encoding:gbk
import sqlite3
import logging

logging.basicConfig(level=logging.INFO,filename = 'mylog.log')
import time
from urllib import urlopen
from urllib import urlretrieve
from HTMLParser import HTMLParser
import re
import os
import time
import datetime
downloadUrl = "http://l-logprocessor1.prod.cn2.corp.agrant.cn/test/AGSmb/"
rootPath_HTML = "downloadHTML"
rootPath_log = "downloadLogs"
print 'linxia'
class MyHTMLParser(HTMLParser):
	def __init__(self, startTime, endTime):
		HTMLParser.__init__(self)
		self.links=[]
		self.linkset = set()
		self.m_startTime = startTime
		self.m_endTime = endTime
	def handle_starttag(self,tag,attrs):
		if not os.path.exists(rootPath_HTML):
			os.mkdir(rootPath_HTML)
		patternDate = re.compile(r'\d{4}(-\d{2}){3}/')
		
		if tag == "a":
			if len(attrs) == 0:
				pass
			else:
				for(variable,value) in attrs:
					if variable == "href":
						if patternDate.match(value):
							#print value
							tdate = time.strptime(value[0:12], "%Y-%m-%d-%H")
							dtdate = datetime.datetime(*tdate[:6])
							if dtdate<self.m_startTime or dtdate>self.m_endTime:
								
								break;
							else:
								dateStr = value[0:7]
								monthPath = rootPath_HTML + os.path.sep + dateStr
								if not os.path.exists(monthPath):
									os.mkdir(monthPath)
								logging.info("start to download url=%s" % ((downloadUrl+value),))	
								retrieveSuccess = False
								while not retrieveSuccess:
									try:
										urlretrieve(downloadUrl+value,monthPath + os.path.sep + value.replace('/','') + ".html")
										if os.path.exists(monthPath + os.path.sep + value.replace('/','') + ".html"):	
											logging.info(monthPath + os.path.sep + value.replace('/','') + ".html exists")
											retrieveSuccess = True
										else:
											retrieveSuccess = False
											logging.info(monthPath + os.path.sep + value.replace('/','') + ".html is not exists")
									
									except Exception,e:
										retrieveSuccess = False
										print e
								logging.info("end download url=%s" % ((downloadUrl+value),))	
								self.parser1 = MyHTMLParser2(value.replace('/',''))
								self.parser1.feed(self.readFile(monthPath + os.path.sep + value.replace('/','') + ".html"))
								self.linkset = self.linkset.union(self.parser1.linkset)
								#print self.linkset
								print "date=",value,"|userCount=", len(self.linkset)
	def readFile(self,filePath):
		fileObject = open(filePath)
		allText = ''
		try:
			allText = fileObject.read()
		finally:
			fileObject.close()
		return allText

class MyHTMLParser2(HTMLParser):
	def __init__(self,date):
		HTMLParser.__init__(self)
		self.links = []
		self.__dateString = date
		self.linkset = set()
		if not os.path.exists(rootPath_log):
			os.mkdir(rootPath_log)
		
	def handle_starttag(self,tag,attrs):
		patternLog = re.compile(r'(.)+\.log')
		if tag == "a":
			if len(attrs) == 0:
				pass
			else:
				for (variable,value) in attrs:
					if variable == "href":
						if patternLog.match(value):
							#print downloadUrl + self.__dateString + "/" + value
							retrieveSuccess = False
							logging.info("start to download url=%s" % ((downloadUrl + self.__dateString + "/" + value),))	
							while not retrieveSuccess:
								try:
									urlretrieve(downloadUrl + self.__dateString + "/" + value,rootPath_log + os.path.sep + value)
									retrieveSuccess = True
									spliteArrays = value.split("-")
									self.linkset.add(spliteArrays[-6:-5][0])
								except Exception,e:
									retrieveSuccess = False 
									print e
							logging.info("end download url=%s" % ((downloadUrl + self.__dateString + "/" + value),))	


etime = datetime.datetime.now()
stime = etime + datetime.timedelta(days=-3)
webpage = urlopen(downloadUrl)
text = webpage.read()
output = open('baidu.html','w')
output.write(text)
output.close()

hp = MyHTMLParser(stime, etime)
hp.feed(text)
hp.close()

print hp.linkset
