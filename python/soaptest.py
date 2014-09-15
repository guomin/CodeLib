#-*- coding: utf-8 -*-
import sys
import zlib
import logging
import traceback as tb
import suds.metrics as metrics
#from tests import *
from suds import WebFault
from suds.client import Client
import base64

def DecodeZipAndBase64String(compstr):
	b = base64.decodestring(compstr)
	unzipstr = zlib.decompress(b, 16+zlib.MAX_WBITS)
	return unzipstr
#
reload(sys)
sys.setdefaultencoding('gbk')
#
#setup_logging()
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)
#logging.getLogger('suds.transport').setLevel(logging.DEBUG)
#logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
#logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)
#logging.getLogger('suds.metrics').setLevel(logging.DEBUG)
#logging.getLogger('suds').setLevel(logging.DEBUG)

url = "https://api.baidu.com/sem/sms/v3/RankService?wsdl"
client = Client(url)

#查看该service提供的方法
#print client
#print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

# 设置认证header
aheader = client.factory.create('ns0:AuthHeader')
#print aheader
aheader.username = ''
aheader.password = ''
aheader.token = ''
client.set_options(soapheaders=aheader)

preViewinfo = client.factory.create('PreviewInfo')
#print preViewinfo
result = client.service.getPreview(["linxia"], 0, 10000, 0, 0, 1, preViewinfo)
#result = client.service.getPreview(["linxia"], 0, 10000, 0, 0, 1)

unzipstr = DecodeZipAndBase64String(result[0].data)
html = unzipstr.decode("UTF-8")

print html.encode("GBK", 'ignore')

import os
#os.system("pause")
