import sys
import time
from bs4 import BeautifulSoup
import requests
from urllib import request


def GPInfo(info):
    print("INFO:", info)


def GPError(num, info):
    print("===ERROR===", num, ':', info)


def GPAct(info):
    print("ACT:", info, "ing...")


def workPath():
    ScriptFilePath = (sys.argv[0])  # 获得的是当前执行脚本的位置（若在命令行执行的该命令，则为空）
    try:
        WorkPathNum = ScriptFilePath.rindex('/')
    except:
        WorkPathNum = ScriptFilePath.rindex('\\')
    WorkPath = ScriptFilePath[0:WorkPathNum + 1]  # 切片
    print("当前工作目录为：" + WorkPath)
    return WorkPath


def get_ip_list():
    url = 'http://www.xicidaili.com/nn/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    url2 = "https://www.2345.com/"
    for i in ip_list:
        proxy_support = request.ProxyHandler({'http': i})
        opener = request.build_opener(proxy_support)
        opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64)")]
        request.install_opener(opener)
        if request.urlopen(url2).read():
            with open("./data/ip.txt", "w")as f:
                f.writelines(i+"\n")
    return ip_list


get_ip_list()


def uA(int):
    list = [
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
        '9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)']
    return list[int]


def timeinfo():
    timea = time.strftime("%Y-%m-%d-%H-%M", time.localtime())  # 获取当前时间
    return timea
