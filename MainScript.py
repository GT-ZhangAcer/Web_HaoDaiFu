from urllib.request import urlopen
from urllib import request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from Tool import *
from lxml import etree
from IP import *
import csv

import traceback  # 错误处理

# UA设置

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}  # 全局UA

key = ['省份名', '城市名', '医院名', '医生信息', '主观疗效', '态度', '评价内容', '花费']  # 数据表头
proxy_S = 0  # 1默认代理 0默认禁止代理
proxynum=19#代理循环数量 填最大代理量即可

def initDriver(idnum):
    try:
        firefoxOpt = Options()  # 载入配置
        firefoxOpt.add_argument("--headless")
        if proxy_S == 1:  # Debug模式下禁用代理
            GPInfo("代理地址为：" + str(proxy[int(int(idnum) % proxynum)]))#只用20个代理IP
            firefoxOpt.add_argument('--proxy-server=http://' + proxy[int(int(idnum) % proxynum)])  # 使用代理
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
    html = urlopen(req, timeout=5)
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
    html = urlopen(req, timeout=5)  # 防假死
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


def doctorList(url,idnum):  # 从更多中获取医生链接列表
    #添加代理
    if proxy_S == 1:
        httpproxy_handler = request.ProxyHandler({"http": 'http://'+proxy[int(int(idnum) % proxynum)]})
        opener = request.build_opener(httpproxy_handler)
        req = request.Request(url, headers=headers)
        html=opener.open(req,timeout=10).read()

    else:
        req = request.Request(url, headers=headers)
        html = urlopen(req, timeout=10)
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
    time.sleep(2)
    GPAct("正在等待系统返回数据")
    page = driver.page_source
    html_BSObj = BeautifulSoup(page, "lxml")  # 链接对象
    # findTittle = (str(html_BSObj.title.text).split("_"))[0]  # 获取标题
    # doctor_about = (html_BSObj.find(attrs={"id": "truncate"})).getText()
    # doctor_about = findTittle + "-" + str(doctor_about)  # 获取医生介绍
    xpathhtml = etree.HTML(page)
    doctor_name = xpathhtml.xpath('//*[@id="doctor_header"]/div[1]/div/a/h1/span[1]/text()')  # 名字
    doctor_keshi = strClean(xpathhtml.xpath(
        '//*[@id="bp_doctor_about"]/div/div[2]/div/table[1]/tbody/tr[2]/td[3]/a/h2/text()'))  # 科室
    doctor_zhicheng = xpathhtml.xpath(
        '//*[@id="bp_doctor_about"]/div/div[2]/div/table[1]/tbody/tr[3]/td[3]/text()')  # 职称
    doctor_shanchang = strClean(xpathhtml.xpath('//*[@id="truncate_DoctorSpecialize"]/text()'))  # 擅长
    # 职业经历
    doctor_Exp = strClean(xpathhtml.xpath('//*[@id="truncate"]/text()'))
    if len(doctor_Exp)<5:
        doctor_Exp = strClean(xpathhtml.xpath('//*[@id="bp_doctor_about"]/div/div[2]/div/table[1]/tbody/tr[5]/td[3]/text()'))

    # 医生是否有照片
    if "n1.hdfimg.com/g2/M03/71/DC/yIYBAFw8OIyAQbw2AAAWC2" in str(strClean(xpathhtml.xpath(
            '//*[@id="bp_doctor_about"]/div/div[2]/div/table[1]/tbody/tr[1]/td/div[1]/table/tbody/tr/td/img')[0])):
        doctor_img = 0  # 没有照片
    else:
        doctor_img = 1  # 有照片

    #医生推荐热度
    doctorHot = strClean(xpathhtml.xpath('//*[@id="bp_doctor_about"]/div/div[2]/div/div[2]/div/div[1]/p[1]/text()'))


    hotpoint1 = str(xpathhtml.xpath('//*[@id="bp_doctor_about"]/div/div[2]/div/div[2]/div/div[2]/p[1]/span[1]/text()'))[
                -5:-2]  # 治疗满意度
    if "00" in hotpoint1:
        hotpoint1 = "100%"
    hotpoint2 = str(xpathhtml.xpath('//*[@id="bp_doctor_about"]/div/div[2]/div/div[2]/div/div[2]/p[2]/span[1]/text()'))[
                -5:-2]  # 态度满意度
    if "00" in hotpoint2:
        hotpoint2 = "100%"

    hotpoint3 = xpathhtml.xpath(
        '//*[@id="bp_doctor_about"]/div/div[2]/div/div[2]/div/div[2]/p[1]/span[2]/text()')  # 累计帮助患者数
    hotpoint4 = xpathhtml.xpath(
        '//*[@id="bp_doctor_about"]/div/div[2]/div/div[2]/div/div[2]/p[2]/span[2]/text()')  # 近两周帮助患者数
    hotnumber = xpathhtml.xpath(
        '//*[@id="hitcnt"]/text()')  # 主页浏览量
    # 感谢信以及礼物数量
    goodnum = xpathhtml.xpath('//*[@id="bp_doctor_about"]/div/div[2]/div/table[1]/tbody/tr[2]/td[4]/a[1]/span/text()')
    giftnum = xpathhtml.xpath('//*[@id="bp_doctor_about"]/div/div[2]/div/table[1]/tbody/tr[2]/td[4]/a[2]/span/text()')

    # 值班时间以及提示
    tips = strClean(xpathhtml.xpath('//*[@id="doctortimebottr"]/tbody/tr[4]/td[2]/text()'))  # 出诊提示
    time_S = xpathhtml.xpath('//*[@id="timeup"]/tbody/tr[2]/td[2]/table[2]/tbody/tr[2]/td')  # 上 中 晚
    time_Z = xpathhtml.xpath('//*[@id="timeup"]/tbody/tr[2]/td[2]/table[2]/tbody/tr[3]/td')  # 此处用*匹配下方所有字符串
    time_W = xpathhtml.xpath('//*[@id="timeup"]/tbody/tr[2]/td[2]/table[2]/tbody/tr[4]/td')

    zhibanTime = []

    def zhiban(obj):
        ii = -1
        num = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        templist = []
        for i in obj:
            htmli = etree.tostring(i, encoding="utf-8", pretty_print=True, method="html")  # Xpath解码 显示中文
            i = BeautifulSoup(htmli, "lxml")
            if "<img" in str(htmli):
                i = i.find('span')
                i = BeautifulSoup(str(i), "lxml").getText()
                templist.append(num[ii] + "挂号费：" + strClean(str(i)))
            ii += 1
        if ii == -1:
            templist.append("无")
        zhibanTime.append(templist)

    zhibanTime.append("上午")
    zhiban(time_S)
    zhibanTime.append("下午")
    zhiban(time_Z)
    zhibanTime.append("晚上")
    zhiban(time_W)
    # 临床数据
    people = xpathhtml.xpath('//*[@id="doctorgood"]/div[2]/table/tbody/tr[1]/td/text()')  # 治疗人数
    peopleing = xpathhtml.xpath('//*[@id="doctorgood"]/div[2]/table/tbody/tr[2]/td/text()')  # 随访人数
    # 投票 函数
    doctor_toupiao = xpathhtml.xpath(
        '/html/body/div[3]/div[1]/div[1]/div[3]/div/div[2]/div/div/div[1]/table/tbody/tr/td')
    doctor_linchuang = xpathhtml.xpath(
        '/html/body/div[3]/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[1]/table/tbody/tr/td')

    toupiao = []
    linchaung = []

    def toupiaodef(info, toupiaoa):
        for i in info:
            i = etree.tostring(i)  # Xpath解码
            iobj = BeautifulSoup(str(i), "lxml")
            toupiaoa.append(strClean(iobj.getText()))

    toupiaodef(doctor_toupiao, toupiao)  # 患者投票
    toupiaodef(doctor_linchuang, linchaung)  # 临床经验
    # 临床经验星级
    star = xpathhtml.xpath('//*[@id="doctorgood"]/div[2]/table/tbody/tr[3]/td/span/img')
    starnum = 0  # 星级计数器
    for i in star:
        i = etree.tostring(i, encoding="utf-8", pretty_print=True, method="html")
        if "liang" in str(i):
            starnum += 1

    # 咨询情况
    zixunUrl = "https:" + strClean(
        xpathhtml.xpath('//*[@id="bp_newthreads"]/div/div[2]/div/div[2]/a/@href')[0])  # 咨询链接获取
    driver.get(zixunUrl)
    driver.implicitly_wait(3)  # 等待JS加载时间
    time.sleep(2)
    page2 = driver.page_source  # 获取当前页面源码
    xpathhtml2 = etree.HTML(page2)
    zixun_people = strClean(xpathhtml2.xpath('/html/body/div[4]/div[2]/div[1]/p/span[2]/span/text()')[0])  # 咨询人数
    html_BSObj = BeautifulSoup(page2, "lxml")
    zixuninfoList = html_BSObj.find(attrs={"class": "zixun_list"})  # 定位信息列表
    xpathhtml2 = etree.HTML(str(zixuninfoList))
    zixuninfo = [zixun_people]
    for i in range(1,10):
        indexstr='//tr['+str(i+1)+']'
        temp1 = xpathhtml2.xpath(indexstr)  # 抓取信息列表
        temp3=etree.tostring(temp1[0], pretty_print=True, method="html")
        temp3=temp3.decode('utf-8')
        temp2 = etree.HTML(str(temp3))
        tempList = []
        tempList.append(strClean(temp2.xpath('//td[2]/p/text()')))  # 名字
        tempList.append(strClean(temp2.xpath('//td[3]/p/a/text()')))  # 问题
        tempList.append(strClean(temp2.xpath('//td[4]/a/text()')))  # 疾病
        tempList.append(strClean(temp2.xpath('//td[5]/text()[1]')[0].replace("(", '')) + "/" + strClean(temp2.xpath('//tr/td[5]/font/text()')))  # 对话数
        zixuninfo.append(tempList)
    # 最后-评论抓取
    pageNumUrl = "https:" + xpathhtml.xpath('//*[@class="lbjg"]/tbody/tr/td/a/@href')[0]  # 获取评论详细页面
    driver.get(pageNumUrl)  # 进入详细评论页
    driver.implicitly_wait(3)  # 等待JS加载时间
    time.sleep(2)
    page = driver.page_source  # 获取当前页面源码
    xpathhtml = etree.HTML(page)
    NowUrl = driver.current_url  # 获取浏览器当前Url
    pagenum = strClean(xpathhtml.xpath('//td[@class="hdf_content"]/div/a[@class="p_text"]/text()')[0])[
              1:-1]  # 没用正则表达式就算好的了将就看吧 嘿嘿嘿（懒） 总评论页数

    def pinglun(pagenum):
        errorTime = 0  # 累了就多休息一下 每错一次就多休息1秒
        for ii in range(1, int(pagenum)):
            if ii % 3 == 2:
                time.sleep(3 + int(errorTime))  # 老规矩 休息一下
            if ii != 1:
                pinglunUrl = str(NowUrl)[:-4] + "/" + str(ii) + ".htm"
            else:
                pinglunUrl = NowUrl
            driver.get(pinglunUrl)
            page = driver.page_source
            html_BSObj = BeautifulSoup(page, "lxml")  # 链接对象
            try:
                find_info = html_BSObj.findAll(attrs={"class": "doctorjy"})  # 获取详细评论
                for i in find_info:
                    html = etree.HTML(str(i))
                    name = html.xpath('//table/tbody/tr[2]/td[2]/table/tbody/tr[1]/td[2]/text()')  # 患者姓名
                    cood = html.xpath('//table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/a/text()')  # 所患疾病
                    think = html.xpath('//table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td/span/text()')  # 看病目的
                    tool = strClean(html.xpath('//table/tbody/tr[2]/td[2]/table/tbody/tr[4]/td/span/text()'))  # 治疗方式
                    attitudeA = html.xpath('//table/tbody/tr[2]/td[2]/table/tbody/tr[5]/td[1]/span/text()')  # 患者主观疗效
                    attitudeB = html.xpath('//table/tbody/tr[2]/td[2]/table/tbody/tr[5]/td[2]/span/text()')  # 态度
                    attitudeC = strClean(html.xpath(
                        '//table/tbody/tr[3]/td[2]/table/tbody/tr[2]/td/text()'))  # 感谢信或看病经验
                    thank = strClean(html.xpath('//table/tbody/tr[3]/td[2]/table/tbody/tr[2]/td/text()')[1:])  # 评价
                    # 该患者的其他分享
                    share1 = strClean(
                        html.xpath('//table/tbody/tr[3]/td[2]/table/tbody/tr[3]/td/div[2]/text()'))  # 选择该医生就诊的理由
                    share2 = strClean(
                        html.xpath('//table/tbody/tr[3]/td[2]/table/tbody/tr[3]/td/div[3]/text()'))  # 本次挂号途径
                    share3 = strClean(
                        html.xpath('//table/tbody/tr[3]/td[2]/table/tbody/tr[3]/td/div[4]/text()'))  # 当前情况
                    money = strClean(html.xpath('//table/tbody/tr[3]/td[2]/table/tbody/tr[3]/td/div[5]/text()'))  # 治疗花费
                    returninfo.append(
                        [doctor_name, doctor_keshi, doctor_zhicheng, doctor_shanchang, doctor_Exp,
                         # 返回[名字 科室 职称 擅长 经历 5
                         hotpoint1, hotpoint2, hotpoint3, hotpoint4, linchaung,  # 疗效满意度 态度满意度 累计帮助患者数 近两周帮助患者数 临床经验统计 5
                         people, peopleing, goodnum, giftnum, starnum,  # 治疗人数 随访人数 感谢信 礼物数量 服务星级4
                         zhibanTime, tips, name, cood, think,  # 值班 出诊提示 患者姓名 症状 看病目的 5
                         tool, attitudeA, attitudeB, attitudeC, thank, share1, share2, share3,
                         # 治疗手段 主观疗效 态度 感谢信&看病经验 评价内容 其它分享x3 8
                         money, toupiao, hotnumber, zixuninfo, doctor_img,doctorHot])  # 花费 投票  主页浏览量 咨询 是否有照片]为每一组的数据  4-32
                    errorTime = 0  # 能走两步了就好好干活！
            except:
                GPError(203, "好像被发现了 休息一下")
                errorTime += 1
                if errorTime % 3 == 2:
                    time.sleep(30)
                continue

    # driver.close()  # 关闭浏览器
    returninfo = []  # 返回数据数组
    pinglun(pagenum)
    return returninfo


# if __name__ == '__main__':

def a():
    def debug():
        global proxy_S
        proxy_S = 0  # 停止代理
        '''
        url="https://www.haodf.com/yiyuan/all/list.htm"
        purlList=pUrl(url)



        url='https://www.haodf.com/yiyuan/beijing/list.htm'
        cityUrlLoad(url)
        url='https://www.haodf.com/yiyuan/beijing/chaoyang/list.htm'
        hUrl(url)
       
        url = 'https://www.haodf.com/hospital/DE4raCNSz6OmG3OUNZWCWNv0.htm'
        print(doctorUrlList(url))
        
        '''
        url='http://www.haodf.com/tuijian/DE4raCNSz6OmG3OUNZWCWNv0/daizhuangpaozhen.htm'
        print(doctorList(url,1))
        '''
        url = 'https://www.haodf.com/doctor/DE4rO-XCoLUmy1568JOrYZEIRi.htm'
        print("Start")
        init_driver = initDriver(0)  # 初始化浏览器对象
        pp = doctorinfo(url, init_driver)
        print(pp)

        init_driver.quit()  # 退出浏览器

        '''
    debug()


#a() #开启Debug模式

# idnum=ID计数器 用于代理、UA计数
if proxy_S == 1:
    try:
        # proxy = getIP()  # 获取代理
        proxy = getLongIpFile()
    except:
        GPError(000, "代理获取失败请重试")

'''
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
'''
