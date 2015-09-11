# -*- coding: cp936 -*-
#以应该从新设计从文章列表入手
import urllib
import urllib2
import re
import os
import time
user_agent = 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
headers={'User-Agent' : user_agent}            
from urllib2 import Request, urlopen, URLError, HTTPError              



class Spider:

    def __init__(self):
        self.siteURL1 = 'http://m.byr.cn/'
        self.siteURL2 = 'http://m.byr.cn/board/Feeling'
        self.siteURL3 = 'http://m.byr.cn/article/Feeling/2789323' 
        self.url1=0
    def geturl(self,num):
        url1 = self.siteURL2
        print url1
        request = urllib2.Request(url1,headers = headers)
        response = urllib2.urlopen(request)
        page1 = response.read().decode('utf-8')
        #pattern1 = re.compile('<li class=.*?<a href="(.*?)">(.*?)</a>.*?</li>',re.S)
        #pattern1 = re.compile('<li>.*?<a href="(.*?)">(.*?)</a>.*?</li>',re.S)
        pattern1 = re.compile('<li>.*?<a href="(.*?)">(.*?)</a>.*?</li>(|)<li class="hl">.*?<a href="(.*?)">(.*?)</a>.*?</li>',re.S)
        items1 = re.findall(pattern1,page1)
        for item1 in items1:
            print item1[0],item1[1]
            url2 = self.siteURL1 + str(item1[0])
            request = urllib2.Request(url2,headers = headers)
            response = urllib2.urlopen(request)
            page1 = response.read().decode('utf-8')
            pattern1 = re.compile('<li.*?<a href="(.*?)">(.*?)</a>.*?"|"</li>.*?</ul>',re.S)
            items1 = re.findall(pattern1,page1)         
        return item1[0]
    def getpagenum1(self):#获取板块首页的总页数
        url1 = self.siteURL2
        print url1
        request = urllib2.Request(url1,headers = headers)
        response = urllib2.urlopen(request)
        page1 = response.read().decode('utf-8')
        #pattern1 = re.compile('<div class="sec nav">.*?<a class="plant">(.*?)/(.*?)</a>.*?"|"<a class="plant">',re.S)
        pattern1 = re.compile('<div class="sec nav">.*?<form action="(.*?)".*?<a class="plant">(.*?)/(.*?)</a>.*?"|"<a class="plant">',re.S)
        result1=re.search(pattern1,page1)
        if result1:
            print result1.group(1),result1.group(3)
            return int(result1.group(3).strip())
        else:          
            return None
    def geturl1(self):#获取板块首页中的连接，每个连接的总帖数（用于计算每贴的页数）
        url1 = self.siteURL2
        print url1
        request = urllib2.Request(url1,headers = headers)
        response = urllib2.urlopen(request)
        page1 = response.read().decode('utf-8')
        #pattern1 = re.compile('<li.*?<div>.*?<a href="(.*?)">(.*?)</a>.*?"((.*?))"</div>',re.S)
        pattern1 = re.compile('<li.*?<a href="(.*?)">(.*?)</a>(.*?)</div>',re.S)
        items = re.findall(pattern1,page1)
        for item in items:
             print item[0],item[1],item[2]
        

    def getPage(self,num,pageIndex):
        url = self.siteURL + str(num)+"?p=" + str(pageIndex)
        self.url1=url
        #print url
        request = urllib2.Request(url,headers = headers)
        try:
            response = urllib2.urlopen(request)
        except URLError,e:
            if hasattr(e,'code'):
                print 'Error code:',e.code
                time.sleep(5)
            elif hasattr(e,'reason'):
                print 'Reason:',e.reason
                time.sleep(5)
        #return response.read().decode('gbk')
        return response.read().decode('utf-8')
#获取帖子用户
    
    def getContents(self,page,user):
        #page = self.getPage(pageIndex)
        pattern = re.compile('<div.*?class="nav hl">.*?<div>.*?<a class="plant">(.*?)</a>.*?"|".*?<a href="/user/query/.*?">(.*?)</a>.*?"|"<a class="plant">',re.S)
        #pattern = re.compile('<div.*?class="nav hl">.*?<a href="/user/query/.*?">(.*?)</a>',re.S)
        #处理输入的用户名
        items = re.findall(pattern,page)
        for item in items:
            matchright=re.match(user,item[1])
            if matchright:
                mytitle=self.getTitle(page)
                f=open(user+'.txt','a+')#w覆盖a后加
                f.writelines(str(mytitle)+'\n'+self.url1+'\n')
                f.close()                
                #print self.url1,item[0] 
            #else:
                #return None
                
#获取帖子标题
    def getTitle(self,page):
       # page = self.getPage(pageIndex)
        pattern1 = re.compile('<ul class="list sec">.*?<li class="f">(.*?)</li>',re.S)
        result=re.search(pattern1,page)
        if result:
            print result.group(1)
            return result.group(1).strip().encode('utf-8')
        else:
            return None
#获取帖子页数
    def getPagenum(self,num,pageIndex):
        url = self.siteURL +str(num)+"?p="+ str(pageIndex)
        self.url1=url
        #print url
        request = urllib2.Request(url,headers = headers)
        try:
            response = urllib2.urlopen(request)
        except URLError,e:
            if hasattr(e,'code'):
                print 'Error code:',e.code
                time.sleep(5)
            elif hasattr(e,'reason'):
                print 'Reason:',e.reason
                time.sleep(5)
        page = response.read().decode('utf-8')
        #获取现在的页数和最后的页数
        pattern1 = re.compile('<div class="sec nav">.*?<form action="(.*?)".*?<a class="plant">(.*?)/(.*?)</a>.*?"|"<a class="plant">',re.S)
        #pattern1 = re.compile('<form action="(.*?)".*?<a href=.*?>',re.S)#文章的二级链接地址
        result1=re.search(pattern1,page)
        if result1:
            #print result1.group(1),result1.group(2),result1.group(3)
            return int(result1.group(3).strip())
        else:          
            return None        
spider = Spider()
#user=raw_input("请输入查询用户：")
#spider.geturl(3)
#spider.getpagenum1()
spider.geturl1()
