from urllib.request import urlopen
from urllib import request
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import re
from Tool import *
from lxml import etree

# UA设置
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}


def initDriver():
    try:
        firefoxOpt = Options()  # 载入配置
        firefoxOpt.add_argument("--headless")
        GPAct("启动浏览器")
        driver = webdriver.Firefox(workPath()+'exe/core/', firefox_options=firefoxOpt)
        GPInfo("浏览器启动成功")
        return driver
    except:
        GPError("001","浏览器启动失败")
        return 1


def pUrl(url):  # 查找省份链接
    req = request.Request(url, headers=headers)
    html = urlopen(req)
    html_BSObj = BeautifulSoup(html, "lxml")  # 链接对象
    find_content = html_BSObj.findAll(attrs={"class": "kstl"})  # 定位目录
    find_url = BeautifulSoup(str(find_content), "lxml")
    find_url = find_url.findAll("a")
    pList = ['北京']  # 因为北京已经展开 所以搜索不到
    pUrl = ['https://www.haodf.com/yiyuan/beijing/list.htm']
    for i in find_url:
        pUrl.append('https://' + str(i.get("href"))[2:])
        pList.append(i.getText())
    info = pList, pUrl  # 省份名 链接
    # print(info)
    return info  # 返回省份名和链接列表


def cityUrlLoad(url):  # 通过省份链接查找城市链接
    req = request.Request(url, headers=headers)
    html = urlopen(req)
    html_BSObj = BeautifulSoup(html, "lxml")  # 链接对象
    find_content = html_BSObj.find(attrs={"class": "ksbd"})  # 定位目录
    find_url = BeautifulSoup(str(find_content), "lxml")
    find_url = find_url.findAll("a")
    cityList = []
    cityUrl = []
    for i in find_url:
        cityUrl.append('https://' + str(i.get("href"))[2:])
        cityList.append(i.getText())
    info = cityList, cityUrl  # 城市名 链接
    # print(info)
    return info  # 返回城市名和链接列表


def hUrl(url):  # 通过城市链接查找医院链接
    req = request.Request(url, headers=headers)
    html = urlopen(req)
    html_BSObj = BeautifulSoup(html, "lxml")  # 链接对象
    find_content = html_BSObj.find(attrs={"class": "m_ctt_green"})  # 定位目录
    find_url = BeautifulSoup(str(find_content), "lxml")
    find_url = find_url.findAll("a")
    hList = []
    hUrl = []
    for i in find_url:
        hUrl.append('https://www.haodf.com/' + str(i.get("href"))[2:])
        hList.append(i.getText())
    info = hList, hUrl  # 医院名 链接
    # print(info)
    return info  # 返回医院名和链接列表


def doctorUrlList(url):  # 获取推荐医生列表页面
    # 医院页面下跳转至医生推荐
    url = url.split("/")[-1:]
    url = 'https://www.haodf.com/tuijian/yiyuan/' + url[0]
    req = request.Request(url, headers=headers)
    html = urlopen(req)
    html_BSObj = BeautifulSoup(html, "lxml")  # 链接对象
    find_content = html_BSObj.find(attrs={"class": "box_a-introList box_a-introList01"})  # 定位目录
    # 定位“更多”
    find_content_obj = BeautifulSoup(str(find_content), "lxml")
    find_more = find_content_obj.findAll(attrs={"rel": 'nofollow'})
    # 定义返回数组
    more_url = []
    for i in find_more:
        more_url.append(i.get("href"))
    ''''# 测试输出
    print("医生链接", url)
    print("更多", find_more)
    print("返回：",more_url)'''

    # 返回 更多 的链接
    return more_url


def doctorList(url):  # 获取医生链接列表
    req = request.Request(url, headers=headers)
    html = urlopen(req)
    html_BSObj = BeautifulSoup(html, "lxml")  # 链接对象
    find_List = html_BSObj.findAll(attrs={"class": "yy_jb_df3"})
    find_a = BeautifulSoup(str(find_List), "lxml")
    find_a = find_a.findAll(attrs={"class": "blue"})
    doctorList = []
    for i in find_a:
        doctorList.append("https://" + str(i.get("href"))[2:])
    return doctorList


def doctorinfo(url, driver):
    driver.get(url)
    driver.implicitly_wait(3)  # 等待JS加载时间
    GPAct("正在等待JS反馈")
    time.sleep(2)
    GPAct("正在等待系统返回数据")
    page = driver.page_source
    html_BSObj = BeautifulSoup(page, "lxml")  # 链接对象
    findTittle = (str(html_BSObj.title.text).split("_"))[0]  # 获取标题

    doctor_about=(html_BSObj.find(attrs={"id":"truncate"})).getText()#获取医生介绍
    find_info = html_BSObj.findAll(attrs={"class": "doctorjy"})  # 获取详细评论
    for i in find_info:
        html = etree.HTML(str(i))
        html_data = html.xpath('//*[@id="comment_type_all"]/table[1]/tbody/tr[2]/td[2]/table/tbody/tr[5]/td[1]/span/text()')
        print(html_data)
    print(doctor_about)



def __init__():
    def debug():
        '''
        url="https://www.haodf.com/yiyuan/all/list.htm"
        purlList=pUrl(url)



        url='https://www.haodf.com/yiyuan/beijing/list.htm'
        cityUrlLoad(url)
        url='https://www.haodf.com/yiyuan/beijing/chaoyang/list.htm'
        hUrl(url)

        url = 'https://www.haodf.com/hospital/DE4raCNSz6OmG3OUNZWCWNv0.htm'
        doctorUrlList(url)
        url='http://www.haodf.com/tuijian/DE4raCNSz6OmG3OUNZWCWNv0/daizhuangpaozhen.htm'
        doctorList(url)'''

        url = 'https://www.haodf.com/doctor/DE4rO-XCoLUmy1568JOrYZEIRi.htm'
        doctorinfo(url,initDriver())

    debug()
    init_shf=0#省份计数器
    init_chs=0#城市总计数器
    init_yy=0#医院总计数器
    init_ys=0#医生总计数器
    init_pl=0#评论总计数器
    def start():
        url = "https://www.haodf.com/yiyuan/all/list.htm"
        purlList = pUrl(url)#获取省份链接
        init_shf=len(purlList[0])
        #for shf in purlList[1]:


__init__()
