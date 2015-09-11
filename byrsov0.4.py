# -*- coding: cp936 -*-
#��Ӧ�ô�����ƴ������б�����
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
    def getpagenum1(self):#��ȡ�����ҳ����ҳ��
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
    def geturl1(self):#��ȡ�����ҳ�е����ӣ�ÿ�����ӵ������������ڼ���ÿ����ҳ����
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
#��ȡ�����û�
    
    def getContents(self,page,user):
        #page = self.getPage(pageIndex)
        pattern = re.compile('<div.*?class="nav hl">.*?<div>.*?<a class="plant">(.*?)</a>.*?"|".*?<a href="/user/query/.*?">(.*?)</a>.*?"|"<a class="plant">',re.S)
        #pattern = re.compile('<div.*?class="nav hl">.*?<a href="/user/query/.*?">(.*?)</a>',re.S)
        #����������û���
        items = re.findall(pattern,page)
        for item in items:
            matchright=re.match(user,item[1])
            if matchright:
                mytitle=self.getTitle(page)
                f=open(user+'.txt','a+')#w����a���
                f.writelines(str(mytitle)+'\n'+self.url1+'\n')
                f.close()                
                #print self.url1,item[0] 
            #else:
                #return None
                
#��ȡ���ӱ���
    def getTitle(self,page):
       # page = self.getPage(pageIndex)
        pattern1 = re.compile('<ul class="list sec">.*?<li class="f">(.*?)</li>',re.S)
        result=re.search(pattern1,page)
        if result:
            print result.group(1)
            return result.group(1).strip().encode('utf-8')
        else:
            return None
#��ȡ����ҳ��
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
        #��ȡ���ڵ�ҳ��������ҳ��
        pattern1 = re.compile('<div class="sec nav">.*?<form action="(.*?)".*?<a class="plant">(.*?)/(.*?)</a>.*?"|"<a class="plant">',re.S)
        #pattern1 = re.compile('<form action="(.*?)".*?<a href=.*?>',re.S)#���µĶ������ӵ�ַ
        result1=re.search(pattern1,page)
        if result1:
            #print result1.group(1),result1.group(2),result1.group(3)
            return int(result1.group(3).strip())
        else:          
            return None        
spider = Spider()
#user=raw_input("�������ѯ�û���")
#spider.geturl(3)
#spider.getpagenum1()
spider.geturl1()
