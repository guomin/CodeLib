#-*- coding: utf-8 -*-
import sys
import zlib
import traceback as tb
import logging
import urllib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("linxia")
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S', )
file_handler = logging.StreamHandler(sys.stderr)
#logger.addHandler(file_handler)
logger.error("daxingtuhao")

from lxml import etree
import codecs

class UtilHelper:
    @staticmethod
    def GetHostName(url):
        retstr = ""
        url = url.replace("http://", "")
        logger.info(url)
        arr1 = url.split("/")
        domainarr= u".com.cn|.net.cn|.org.cn|.gov.cn|.com|.net|.cn|.org|.cc|.me|.tel|.mobi|.asia|.biz|.info|.name|.tv|.hk|.公司|.中国|.网络".encode("utf-8").split('|');
        for domain in domainarr:
            if arr1[0].endswith(domain):
                replaceStr = arr1[0].replace(domain, "")
                #print replaceStr
                if '.' in replaceStr and replaceStr.index('.') > 0:
                    replaceArr = replaceStr.split('.')
                    returnStr = replaceArr[len(replaceArr)-1]+domain
                    
                    #if 二级域名
                    if len(replaceArr) > 1:
                        if replaceArr[len(replaceArr)-2] != "www":
                            returnStr = replaceArr[len(replaceArr)-2]+"."+returnStr;
                    
                    return returnStr;
                else:
                    returnStr = replaceStr + domain;
                    return returnStr;
            returnStr = url
            
        return url;
                
            
                
        
            
        
        
        return retstr;

class TemplateHelper:
    def __init__(self):
        print ""
    def GetTempLate(self, fname):
        f = codecs.open(fname, "r", "utf-8")
        content = f.read()
        f.close()
        templates = etree.XML(content.encode('utf-8'))
        return templates;

class RankInfo:
    def __init__(self):
        self.webNameField = "";
        self.urlField = "";
        self.seoPosField = -1;
        self.semPosField = -1;
        self.semNumField = 0;
        self.semTypeField = 0;
        self.isLeftField = 0;
        self.positionField = 0;
        self.title = "";
        self.idea = "";
        self.rankPosition = 0;
        self.redWords = []; 
        
class KeywordResult:
    def __init__(self):
        self.totalPages = 0;
        self.totalResults = 0;
        self.rankInfoSet = [];

        
        
class BaiduCrawler:
    def __init__(self):
        self.logger = logging.getLogger("BaiduCrawler")
        tHelper = TemplateHelper() 
        self.leftTopTemplateDoc = tHelper.GetTempLate("leftTopTemplate.xml")
        #self.rightTemplateDoc = tHelper.GetTempLate("");
        #self.leftContentTemplateDoc = tHelper.GetTempLate("");
    def AnalyzeHeader(self, tree):
        #
        totalResults = 0
        try:
            node = tree.xpath(".//div[@class='nums']");
            if 1:
                astr = str(node[0].text)
                astr = astr.replace(u"百度为您找到相关结果", "")
                astr = astr.replace(u"约", "");
                astr = astr.replace(u"个", "")
                astr = astr.replace(u",", "")
                totalResults = int(astr)
        except:
            self.logger.error("AnalyzeHeader error")
        finally:
            print totalResults
            
        return totalResults
        
    def AnalyzeLeftTop(self, tree):
        leftTopTemplateMatch = False
        rankInfoSet = []
        leftTopTemplateList = self.leftTopTemplateDoc.xpath("//template")
        leftTopContainer = ""
        for leftTopTemplate in leftTopTemplateList:
            leftTopTemplateMatch = False
            leftTopTemplateContainerPathNodes = leftTopTemplate.xpath("./containerPath")
            for leftTopTemplateContainerPathNode in leftTopTemplateContainerPathNodes:
                #leftTopContainer = 
                print "jiexi"
                print leftTopTemplateContainerPathNode.text
                leftTopContainer = tree.xpath(leftTopTemplateContainerPathNode.text.encode('utf-8'))
                if leftTopContainer:
                    break;
            if not(leftTopContainer):
                continue;
            leftTopTemplateNodes = leftTopTemplate.xpath("./node")
            for leftTopTemplateNode in leftTopTemplateNodes:
                leftTopTitlePath = []
                leftTopIdeaPath = []
                leftTopUrlPath = []
                leftTopTemplateTitlePathList = leftTopTemplateNode.xpath("./title/titlePath")
                leftTopTemplateIdeaPathList = leftTopTemplateNode.xpath("./idea/ideaPath")
                leftTopTemplateUrlPathList = leftTopTemplateNode.xpath("./url/urlPath")
                for leftTopTemplateTitlePath in leftTopTemplateTitlePathList:
                    leftTopTitlePath.append(leftTopTemplateTitlePath)
                for leftTopTemplateIdeaPath in leftTopTemplateIdeaPathList:
                    leftTopIdeaPath.append(leftTopTemplateIdeaPath);
                for leftTopTemplateUrlPath in leftTopTemplateUrlPathList:
                    leftTopUrlPath.append(leftTopTemplateUrlPath);
                    
                leftTopNodePath = leftTopTemplateNode.xpath("./nodePath")[0].text
                print leftTopNodePath
                leftTopNodes = leftTopContainer[0].xpath(leftTopNodePath)
                if leftTopNodes:
                    nodeNum = 0
                    for leftTopNode in leftTopNodes:
                        nodeNum += 1
                        rankInfo = RankInfo()
                        redWords = []
                        rankInfo.isLeftField = 1
                        #rankInfo.semTypeField = int(leftTopTemplateNode.attribs)
                        rankInfo.seoPosField = 0
                        leftTopTitleNode = []
                        leftTopIdeaNode = []
                        leftTopUrlNode = []
                        i = 0
                        while True:
                            leftTopTitleNode = leftTopNode.xpath(leftTopTitlePath[i].text)
                            i += 1
                            if i>=len(leftTopTitlePath):
                                break;
                            if leftTopTitleNode:
                                break;
                        i = 0
                        while True:
                            leftTopIdeaNode = leftTopNode.xpath(leftTopIdeaPath[i].text)
                            i += 1
                            if i>=len(leftTopIdeaPath):
                                break;
                            if leftTopIdeaNode:
                                break;
                        i = 0
                        while True:
                            leftTopUrlNode = leftTopNode.xpath(leftTopUrlPath[i].text)
                            i += 1
                            if i>=len(leftTopUrlPath):
                                break;
                            if leftTopUrlNode:
                                break;
                        
                        if leftTopTitleNode:
                            rankInfo.title = etree.tostring(leftTopTitleNode[0], method='text', encoding='utf-8')
                        else:
                            rankInfo.title = "";    
                        if leftTopIdeaNode:
                            rankInfo.idea = leftTopIdeaNode[0].text
                        else:
                            rankInfo.idea = ""
                        if leftTopUrlNode:
                            rankInfo.urlField = leftTopUrlNode[0].text
                        else:
                            rankInfo.urlField = "";
                        if rankInfo.urlField != "":
                            rankInfo.webNameField = UtilHelper.GetHostName(rankInfo.urlField);
                        else:
                            rankInfo.webNameField = ""
                        leftTopTitleRedNodes = ""
                        # todo 标红词处理
                        
                        rankInfo.rankPosition = 0;
                        rankInfo.redWords = []
                        rankInfoSet.append(rankInfo);
                    leftTopTemplateMatch = True;
            if leftTopTemplateMatch:
                break;
            
        if not(leftTopTemplateMatch):
            rankInfoSet = []
        return rankInfoSet        
                    
    def AnalyzeLeftContent(self, tree):
        print ""
        
    def AnalyzeRight(self, tree):
        print ""
        
    def AnalyzeFooter(self, tree):
        totalPages = 0
        try:
            node = tree.xpath(".//*[@id='page']")
            # todo
            print etree.tostring(node[0], method="text", encoding="utf-8")
        except:
            self.logger.error("AnalyzeFooter error")
            
        return totalPages
        
    def AnalyzeAll(self, rankInfoSet):
        print ""
        
        
    def Parse(self, html):
        rightTemplateMatch = False;
        leftTopTemplateMatch = False;
        leftContentTemplateMatch = False;
        
        if "from action=\"http://verify.baidu.com/verify\"" in html:
            return False
        
        totalResults = 0;
        totalPages = 0;
        kwResult = KeywordResult()
        rankInfoSet = []
        tree = etree.HTML(html)
        
        try:
            totalResults = self.AnalyzeHeader(tree)
            rankInfoSet.append(self.AnalyzeLeftTop(tree))
            rankInfoSet.append(self.AnalyzeLeftContent(tree))
            rankInfoSet.append(self.AnalyzeRight(tree))
            totalPages = self.AnalyzeFooter(tree)
            
            rankInfoSet = self.AnalyzeAll(rankInfoSet)
            
        finally:
            print ""
            
        kwResult.totalResults = totalResults
        kwResult.totalPages = totalPages
        kwResult.rankInfoSet = rankInfoSet
        
        return kwResult

def test(filename):
    fname = filename
    f=codecs.open(fname, "r", "utf-8")
    content = f.read()
    f.close()
    

    tree = etree.HTML(content)

    templateList = tree.xpath(u".//div[@id='content_left']")
    nodeList = templateList[0].xpath(u".//div[parent::div[@id='content_left'] and descendant::a[text()[1]='推广' and not(text()[2]) and not(em)] and (not(@tpl) or @tpl!=\"ecl_health_mix_page\") and  not(contains(@style, 'display:none')) and  child::div[position()=2 and not(contains(@class, 'oc-hide'))]]")
    titleList = nodeList[0].xpath(u"./div[1]/h3[1]/a[1]")

    print titleList[0].text

    title = etree.tostring(titleList[0], method="text", encoding="utf-8")
    print title

    #import os
    #os.system("pause")
    
def test2(filename):
    fname = filename
    f=codecs.open(fname, "r", "utf-8")
    content = f.read()
    f.close()
    
    crawler = BaiduCrawler()
    #crawler.Parse(content)
    riset = crawler.AnalyzeLeftTop(etree.HTML(content))
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n\n"
    for ri in riset:
        print "url:\t"+ri.urlField
        print "main domain name:\t"+ri.webNameField
        print "title:\t"+ri.title
        #print "idea:\t"+ri.idea
    
    print "..."
    
def test3(url):
    url = "http://baidu.com"
    print UtilHelper.GetHostName(url)
    url = "www2.baidu.com"
    print UtilHelper.GetHostName(url)
    url = "www.baidu.com.cn"
    print UtilHelper.GetHostName(url)
    url = "http://beijing.homelink.com.cn"
    print UtilHelper.GetHostName(url)
    
if __name__=="__main__":
    #test2(u"C:/Users/guomin/Desktop/tmp/OTHER_BAIDU_二手房_20140910_165744351.html")  
    test2(u"C:/Users/guomin/Desktop/tmp/限时秒杀_百度搜索.htm")
    #test3("")

