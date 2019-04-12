from bs4 import BeautifulSoup
from lxml import etree
from urllib import request
from urllib.request import urlopen
import time
from Tool import *


def getUA(num):
    headers = [{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'},
               {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
               {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'},
               {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"},
               {'User-Agent': "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11"},
               {'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"},
               {'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"},
               {'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"},
               {'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)"},
               {'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"}
               ]
    return headers[num]



# 全局UA

def getIP():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}
    url = "https://ip.seofangfa.com"
    req = request.Request(url, headers=headers)
    html = request.urlopen(req, timeout=5)


    html_BSObj = BeautifulSoup(html, "lxml")
    xpathhtml = etree.HTML(str(html_BSObj))
    iplist = []

    for i in range(1, 25):
        tempip = xpathhtml.xpath("//table/tbody[1]/tr[" + str(i) + "]/td[1]/text()")  # IP
        temppost = xpathhtml.xpath("//table/tbody[1]/tr[" + str(i) + "]/td[2]/text()")  # 端口
        iplist.append(str(tempip[0]) + ":" + str(temppost[0]))

    print("可用代理数量：", len(iplist)+1)
    return iplist#返回IP:端口列表

def getLongIpFile():
    with open('./IP/ip.txt','r') as f:
        ipList=str(f.read()).split("\n")
        print("可用代理数量：", len(ipList))
        return ipList


class proxyc:
    i = 0  # 循环计数器 达到proxynum数量则重新获取代理
    api = []
    proxynum=1#代理循环数

    #先初始化得到代理
    def __init__(self,proxynum):
        self.findapi()
        self.proxynum=proxynum

    #从API获取代理
    def findapi(self):
        url = "http://www.66ip.cn/mo.php?sxb=&tqsl=1000&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea="
        req = request.Request(url)
        html = urlopen(req, timeout=5)
        html = BeautifulSoup(html, "lxml")
        xpathhtml = etree.HTML(str(html))
        html = xpathhtml.xpath("/html/body")
        apiList = etree.tostring(html[0])
        apiList = str(apiList).split("<br/>")

        for i in apiList[5:-50]:
            self.api.append(
                i.replace("&#13;", "").replace('\\t', "").replace('\\n', "").replace("&", "").replace("#", "").replace(
                    '\\', ""))

    #弹出一个代理
    def findProxy(self):
        proxyinfo = self.api[self.i]
        self.i += 1
        if self.i == self.proxynum - 20:
            self.findapi()
            self.i=0
        print(self.i)
        return proxyinfo

    #出错之后弹出下一个代理
    def error(self):
        self.i += 1