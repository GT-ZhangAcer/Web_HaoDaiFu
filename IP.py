from bs4 import BeautifulSoup
from lxml import etree
from urllib import request
import time
from Tool import *


def getUA(num):
    headers = [[{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}],
               [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}],
               [{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'}],
               [{'User-Agent': "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"}],
               [{'User-Agent': "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11"}],
               [{'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"}],
               [{'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"}],
               [{'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"}],
               [{'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)"}],
               [{'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"}]
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
    return iplist