from urllib.request import urlopen
from urllib import request
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import re
from Tool import *
from lxml import etree

import csv

import traceback  # 错误处理

# UA设置

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}  # 全局UA

key = ['省份名', '城市名', '医院名', '医生信息', '主观疗效', '态度', '评价内容', '花费']  # 数据表头


def initDriver():
    try:
        firefoxOpt = Options()  # 载入配置
        firefoxOpt.add_argument("--headless")
        GPAct("启动浏览器")
        driver = webdriver.Firefox(workPath() + 'exe/core/', firefox_options=firefoxOpt)
        GPInfo("浏览器启动成功")
        return driver
    except:
        GPError("001", "浏览器启动失败")
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


def doctorList(url):  # 从更多中获取医生链接列表
    req = request.Request(url, headers=headers)
    html = urlopen(req)
    html_BSObj = BeautifulSoup(html, "lxml")  # 链接对象
    find_List = html_BSObj.findAll(attrs={"class": "yy_jb_df3"})
    find_a = BeautifulSoup(str(find_List), "lxml")
    find_a = find_a.findAll(attrs={"class": "blue"})
    doctorList = []
    for i in find_a:
        doctorList.append("https://" + str(i.get("href"))[2:])
    return doctorList  # 返回医生详情页链接


def doctorinfo(url, driver):  # 查找评价
    driver.get(url)
    driver.implicitly_wait(3)  # 等待JS加载时间
    GPAct("正在等待JS反馈")
    time.sleep(2)
    GPAct("正在等待系统返回数据")
    page = driver.page_source
    html_BSObj = BeautifulSoup(page, "lxml")  # 链接对象
    findTittle = (str(html_BSObj.title.text).split("_"))[0]  # 获取标题
    doctor_about = (html_BSObj.find(attrs={"id": "truncate"})).getText()
    doctor_about = findTittle + "-" + str(doctor_about)  # 获取医生介绍
    find_info = html_BSObj.findAll(attrs={"class": "doctorjy"})  # 获取详细评论

    returninfo = []
    for i in find_info:
        html = etree.HTML(str(i))
        attitudeA = html.xpath('//table/tbody/tr[2]/td[2]/table/tbody/tr[5]/td[1]/span/text()')  # 患者主观疗效
        attitudeB = html.xpath('//table/tbody/tr[2]/td[2]/table/tbody/tr[5]/td[2]/span/text()')  # 态度
        thank = html.xpath('//table/tbody/tr[3]/td[2]/table/tbody/tr[2]/td/text()')[1:]  # 评价
        money = html.xpath('//table/tbody/tr[3]/td[2]/table/tbody/tr[3]/td/div[5]/text()')  # 治疗花费
        returninfo.append([doctor_about, attitudeA, attitudeB, thank, money])
    # driver.close()  # 关闭浏览器
    return returninfo  # 返回[医生信息 主观疗效 态度 评价内容 花费]为每一组的数据


def __init__():
    def debug():
        '''
        url="https://www.haodf.com/yiyuan/all/list.htm"
        purlList=pUrl(url)



        url='https://www.haodf.com/yiyuan/beijing/list.htm'
        cityUrlLoad(url)
        url='https://www.haodf.com/yiyuan/beijing/chaoyang/list.htm'
        hUrl(url)
       '''
        url = 'https://www.haodf.com/hospital/DE4raCNSz6OmG3OUNZWCWNv0.htm'
        print(doctorUrlList(url))

        '''
        url='http://www.haodf.com/tuijian/DE4raCNSz6OmG3OUNZWCWNv0/daizhuangpaozhen.htm'
        print(doctorList(url)) 

        url = 'https://www.haodf.com/doctor/DE4rO-XCoLUmy1568JOrYZEIRi.htm'
        init_driver = initDriver()  # 初始化浏览器对象
        doctorinfo(url, init_driver)
        init_driver.quit()  # 退出浏览器'''

    # debug()

    def start():
        error1 = 1
        error2 = 1
        init_driver = initDriver()  # 初始化浏览器对象
        # global headers
        csvName = str(timeinfo()) + ".csv"
        with open(csvName, 'w', newline='') as f:  # 数据准备写入
            writer = csv.DictWriter(f, key)
            writer.writeheader()

            url = "https://www.haodf.com/yiyuan/all/list.htm"
            purlList = pUrl(url)  # 获取省份链接

            init_shf = 0  # 省份总计数器
            init_chs = 0  # 城市总计数器
            init_yy = 0  # 医院总计数器
            init_ys = 0  # 医生总计数器
            init_pl = 0  # 评论总计数器

            init_shf = len(purlList[0])
            for temp_shf in range(init_shf):
                shfName = purlList[0][temp_shf]  # 省份名
                shfUrl = purlList[1][temp_shf]  # 省份链接
                cityInfoList = cityUrlLoad(shfUrl)  # 获取城市链接
                init_chs += len(cityInfoList[0])
                try:
                    for temp_chs in range(len(cityInfoList[0])):
                        chsName = cityInfoList[0][temp_chs]  # 城市名
                        chsUrl = cityInfoList[1][temp_chs]  # 城市链接
                        hostipal = hUrl(chsUrl)
                        init_yy += len(hostipal[0])
                        i = 0
                        if init_yy % 3 == 0:
                            GPAct("防止反爬检测，暂停进行等待")
                            GPInfo("当前状态：第" + str(temp_shf+1) + "个省份")
                            time.sleep(20)
                        try:
                            for temp_yy in range(len(hostipal[0])):
                                hostipalName = hostipal[0][temp_yy]  # 医院名
                                hostipalUrl = hostipal[1][temp_yy]  # 医院链接
                                doctorUrl = doctorUrlList(hostipalUrl)
                                i += 1
                                if i % 3 == 0:
                                    # headers = uA(init_yy % 9)
                                    GPAct("防止反爬检测")
                                    time.sleep(30)
                                try:
                                    for temp_url in doctorUrl:
                                        doctorUrll = doctorList(temp_url)
                                        init_ys += len(doctorUrll)
                                        for temp_ys in range(len(doctorUrll)):
                                            if temp_ys % 5 == 0:
                                                # headers = uA(init_yy % 9)
                                                GPAct("防止反爬检测")
                                                time.sleep(10)
                                            url = doctorUrll[temp_ys]  # 医生链接
                                            info = doctorinfo(url, driver=init_driver)  # 获取信息
                                            for i in info:
                                                finalInfo = {'省份名': shfName,
                                                             '城市名': chsName,
                                                             '医院名': hostipalName,
                                                             '医生信息': i[0],
                                                             '主观疗效': i[1],
                                                             '态度': i[2],
                                                             '评价内容': i[3],
                                                             '花费': i[4]}
                                                writer.writerow(finalInfo)
                                                init_pl += 1
                                                if init_pl % 30 == 0:
                                                    error1 -= 1
                                                    error2 -= 2
                                                    init_driver.quit()
                                                    init_driver = initDriver()  # 重新开浏览器
                                except:
                                    GPError("997", traceback.format_exc())
                                    continue


                        except:
                            error1 += 1
                            if error1 % 5 == 0:
                                GPError("200", "被发现了，暂停3分钟")
                                time.sleep(180)
                            GPError("998", traceback.format_exc())
                            continue
                except:
                    error2 += 1
                    if error2 % 5 == 0:
                        GPError("200", "被发现了，暂停3分钟")
                        time.sleep(180)
                    GPError("999", traceback.format_exc())
                    continue

        GPInfo("共成功抓取 城市数：" + str(init_chs) + "医院数：" + str(init_yy) + "医生数：" + str(init_ys) + "评论数：" + str(init_pl))
        init_driver.quit()

    start()


__init__()
