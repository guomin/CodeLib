#encoding:gbk
import httplib
import time
from HTMLParser import HTMLParser
import urllib,re,json
url = "/login?service=http://xuri.p4p.sogou.com"
def gethttpresponse(method,host,queryString,body={},cookie=""):
	headersDic = {}	
	headersDic["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0"	
	headersDic["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
	headersDic["Accept-Language"] = "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3"
	headersDic["Accept-Encoding"] = "gzip, deflate"
	headersDic["Content-Type"] = "application/x-www-form-urlencoded"
	headersDic["Host"] = host
	#headersDic["DNT"] = "1"
	headersDic["Connection"] = "keep-Alive"
	#conn = httplib.HTTPConnection(host)
	conn = httplib.HTTPConnection('127.0.0.1',8888)
	if cookie != "": 
		headersDic["Cookie"] = cookie
	if method.lower() == "post":
		print body
		body=urllib.urlencode(body)
		print "--------------------"
		print body
	if method.lower() == "post":
		conn.request(method,queryString,body,headersDic)
	else:
		conn.request(method,queryString,None,headersDic)
	res = conn.getresponse()
	return res
def gethttpsresponse(method,host,queryString,body={},cookie=None):
	headersDic = {}	
	headersDic["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0"	
	headersDic["Accept"] = "text/html, application/xhtml+xml, */*"
	headersDic["Accept-Language"] = "zh-CN"
	headersDic["Accept-Encoding"] = "gzip, deflate"
	headersDic["Content-Type"] = "application/x-www-form-urlencoded"
	headersDic["Host"] = host
	headersDic["DNT"] = "1"
	headersDic["Connection"] = "keep-Alive"
	conn = httplib.HTTPSConnection(host)
	if cookie is not None:
		headersDic["Cookie"] = cookie
	if method.lower() == "post":
		print body
		body=urllib.urlencode(body)
		print "--------------------"
		print body
	if method.lower() == "post":
		conn.request(method,queryString,body,headersDic)
	else:
		conn.request(method,queryString,None,headersDic)
	res = conn.getresponse()
	return res
def get_location(responseHeaders):
	location = ""
	for key,value in responseHeaders:
		if key == "location":
			location = value
	return location
def get_cookie(responseHeaders):
	cookie = ""
	for key,value in responseHeaders:
		if key == "set-cookie":
			cookie = value
	return cookie

def httpsrequest(method,host,queryString,cookie="",referer="",body={}):
	headersDic = {}	
	headersDic["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0"	
	headersDic["Accept"] = "text/html, application/xhtml+xml, */*"
	headersDic["Accept-Language"] = "zh-CN"
	headersDic["Accept-Encoding"] = "gzip, deflate"
	headersDic["Content-Type"] = "application/x-www-form-urlencoded"
	headersDic["Host"] = host
	headersDic["DNT"] = "1"
	headersDic["Connection"] = "keep-Alive"
	if cookie != '': 
		headersDic["Cookie"] = cookie
	headersDic["Referer"] = referer
	conn = httplib.HTTPSConnection(host)
	print '------------------header-----------------'
	print headersDic
	print '-----------------------------------------'
	if method.lower() == "post":
		print body
		body=urllib.urlencode(body)
		print "--------------------poststart----------------"
		print body
		print "--------------------postend------------------"
	conn.request(method,queryString,body,headersDic)
	res = conn.getresponse()
	resheaders = res.getheaders()
	print resheaders
	status = res.status
	data = res.read() 
	if status == 200:
		pass
	else:
		print "http response code(%s):%s" % (status,res.reason)
	return data



class MyHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.links = []
		self.tags = {}
		self.src = ""
		self.hiddenDic = {} 
	def handle_starttag(self,tag,attrs):
		if not self.tags.has_key(tag):
			self.tags[tag] = attrs
		if tag == "img":
			isCodeImage = False
			for attr in attrs:
				if attr[0] == "id" and attr[1] == "validateCodeImg":
					isCodeImage = True
					break
			if isCodeImage:
				for attr in attrs:
					if attr[0] == "src":
						self.src = attr[1]
		if tag == "input":
			is_hidden_type = False
			for attr in attrs:
				if attr[0] == "type" and attr[1] == "hidden":
					is_hidden_type = True
			if is_hidden_type:
				name = ""
				value = ""
				for attr in attrs:
					if attr[0] == "name":
						name = attr[1]
					elif attr[0] == "value":
						value = attr[1]
				self.hiddenDic[name] = value

import StringIO,gzip

def gzdecode(data):
	compressdstream = StringIO.StringIO(data)
	gziper = gzip.GzipFile(fileobj = compressdstream)
	data2 = gziper.read()
	return data2

#print help(httplib.HTTPConnection) 
print help(httplib.HTTPConnection.request)
##################################################################################################
res = gethttpsresponse("GET","auth.p4p.sogou.com","/login?service=http://xuri.p4p.sogou.com",None)
resHeaders = res.getheaders()
location = get_location(resHeaders)
cookie = get_cookie(resHeaders)
loginpage = res.read()#httpsrequest("GET","auth.p4p.sogou.com","/login?service=http://xuri.p4p.sogou.com","","/login?service=http://xuri.p4p.sogou.com")
parser = MyHTMLParser()
parser.feed(loginpage)
conn = httplib.HTTPSConnection("auth.p4p.sogou.com")

conn.request("GET",parser.src,None,{"cookie":cookie})
try:
	f = open("code.jpg",'wb')
	f.write(conn.getresponse().read())
finally:
	f.close()
code = raw_input("Please input code : ")
parser.hiddenDic["validateCode"] = code
parser.hiddenDic["username"] = "******"
parser.hiddenDic["password"] = "******"
result = httpsrequest("POST","auth.p4p.sogou.com","/login?service=http://xuri.p4p.sogou.com",cookie,"/login?service=http://xuri.p4p.sogou.com",parser.hiddenDic)
pattern = re.compile(r'"http://(.)+"')
ma1 = pattern.search(result)
print ma1.group()
if ma1:
	url = ma1.group().strip('"')
	print 'access %s' % (url,)	
	print url[len("http://xuri.p4p.sogou.com"):]
	res_url = gethttpresponse("GET","xuri.p4p.sogou.com","/" + url[len("http://xuri.p4p.sogou.com"):],"")
	uncompresed = gzdecode(res_url.read())
	print "uncompresed data:"
	print uncompresed
	if "/index/init.action" in uncompresed:
		res_cookie = get_cookie(res_url.getheaders())
		print res_cookie
		res_action = gethttpresponse("GET","xuri.p4p.sogou.com","/index/init.action",{},res_cookie)
		html_action = gzdecode(res_action.read())
		try:
			actionFile = open("sougouaction.html","w")
			actionFile.write(html_action)
		finally:
			actionFile.close()
		cpcadindex_action = gethttpresponse("GET","xuri.p4p.sogou.com","/cpcadindex/init.action",{},res_cookie)
		print get_cookie(cpcadindex_action.getheaders())
		html_cpcadindex = gzdecode(cpcadindex_action.read())
		try:
			cpcadindexFile = open("sogou_cpcadindexFile.html","w")
			cpcadindexFile.write(html_cpcadindex)
		finally:
			cpcadindexFile.close()
		res_getip = gethttpresponse("GET","xuri.p4p.sogou.com","/tool/adlive/getIp.action",{},res_cookie)
		json_getip = gzdecode(res_getip.read())
		decodejson = json.loads(json_getip)
		ipDic = {}
		for key,value in decodejson.items():
			if key == 'data':
				for item in value:
					province = ''
					ip = ''
					for key2,value2 in item.items():
						if key2 == 'province':
							province = value2
						elif key2 == 'ip':
							ip = value2
					print "%s|%s" % (province,ip)
					#province = province.encode('gbk')
					ipDic[province] = ip
					#print urllib.urlencode(r'租车')
					#print ipDic['北京']
		print '北京'
		print ipDic[u'北京']
		adkey = 'apple'
		ps = {'adkey':adkey,'page':1,'ip':ipDic[u'北京']}
		requestQuery = ("/tool/adlive/previewPage.action?%s" % urllib.urlencode(ps))
		requestQuery = "/tool/adlive/previewPage.action?adKey=apple&page=1&ip=61.135.188.225";
		res_preview = gethttpresponse("GET","xuri.p4p.sogou.com",requestQuery,{},res_cookie)
		html_preview = gzdecode(res_preview.read())
		print res_preview.getheaders()
		html_preview = html_preview.decode('utf-8')
		print html_preview
		try:
			cpcadindexFile = open("sogou_preview_"+str(int(time.time()))+".html","w")
			cpcadindexFile.write(html_preview.encode('utf-8'))
		finally:
			cpcadindexFile.close()
	#	res_getip = gethttpresponse("GET","xuri.p4p.sogou.com","/tool/adlive/getIp.action",{},res_cookie)
	#	print html_getip
	#	print html_cpcadindex
	#	print html_action

end = raw_input("stop")


