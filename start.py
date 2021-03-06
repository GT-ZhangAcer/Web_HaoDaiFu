from MainScript import *
import threading
from visualdl import LogWriter
from proxy.proxy.IP import proxyc  # 引入代理包
import csv

key0 = ['省份名', '城市名', '医院名', '医院Url', ]  # 数据表头 0-3
key1 = ['省份名', '城市名', '医院名', '医生Url', '医生ID']  # 数据表头 0-3
key2 = ['医生ID', '省份名', '城市名', '医院名', '医生姓名',  # 1+3+1
        '科室', '职称', '擅长', '经历', '疗效满意度',  # 5
        '态度满意度', '累计帮助患者数', '近两周帮助患者数',  # 3
        '临床经验统计', '治疗人数', '随访人数', '感谢信', '礼物数量', '服务星级',  # 6
        '值班', '出诊提示', '患者姓名', '症状', '看病目的',  # 5
        '治疗手段', '主观疗效', '感谢信&看病经验', '态度', '评价内容', '就诊理由', '挂号途径', '当前情况',  # 8
        '花费', '投票', '评论时间', '主页浏览量', '咨询信息列表', '照片', '推荐热度']  # 5 数据表头 0-4-34
# 记录可视化日志
logw = LogWriter("c:/log/main_log", sync_cycle=2)
with logw.mode('抓取总数') as logger:
    allTag = logger.scalar("总概览")
with logw.mode('错误总数') as logger:
    allErrorTag = logger.scalar("总概览")

# visualDL --logdir c:/log/main_log --port 8080 --host 127.0.0.10

# 浏览器设定
proxy_S = 1  # 1默认代理 0默认禁止代理
proxynum = 500  # 代理循环数量 填最大代理量即可
idnum = 0  # 设备指纹

# idnum=ID计数器 用于代理、UA计数

if proxy_S == 1:
    # try:
    # proxy = getIP()  # 获取代理
    # proxy = getLongIpFile()
    proxy = proxyc(proxynum=proxynum, key="GKASLPADKLQCVDFDHVI")  # 实例化代理获取器


# except:
# GPError(000, "代理获取失败请重试")


def initDriver(proxyinfo):  # 传入代理地址
    firefoxOpt = Options()  # 载入配置
    global idnum
    firefoxOpt.add_argument("--headless")
    while (1):
        try:
            if proxy_S == 1:  # Debug模式下禁用代理

                GPInfo("代理地址为：" + str(proxyinfo))
                firefoxOpt.add_argument('--proxy-server=http://' + str(proxyinfo))  # 使用代理
            GPAct("启动浏览器")
            driver = webdriver.Firefox(workPath() + 'exe/core/', firefox_options=firefoxOpt)
            GPInfo("浏览器启动成功")
            # GPInfo("当前指纹为：" + str(idnum))
            idnum += 1
            return driver
        except:
            GPError("999", traceback.format_exc())
            GPError("001", "浏览器启动失败")
            idnum += 1
            continue


# 抓取主循环
def savehostipalList():
    csvName = "./data/ALLHostipalUrl" + str(timeinfo()) + ".csv"
    with open(csvName, 'w', newline='', encoding='utf-8') as f:  # 数据准备写入
        writer = csv.DictWriter(f, key0)
        writer.writeheader()

        url = "https://www.haodf.com/yiyuan/all/list.htm"
        purlList = pUrl(url)  # 获取省份链接

        init_chs = 0  # 城市总计数器
        init_yy = 0  # 医院总计数器

        init_shf = len(purlList[0])
        for temp_shf in range(init_shf):
            shfName = purlList[0][temp_shf]  # 省份名
            shfUrl = purlList[1][temp_shf]  # 省份链接
            cityInfoList = cityUrlLoad(shfUrl)  # 获取城市链接
            init_chs += len(cityInfoList[0])
            for temp_chs in range(len(cityInfoList[0])):
                chsName = cityInfoList[0][temp_chs]  # 城市名
                chsUrl = cityInfoList[1][temp_chs]  # 城市链接
                hostipal = hUrl(chsUrl)
                init_yy += len(hostipal[0])
                if init_yy % 3 == 0:
                    GPAct("防止反爬检测，暂停进行等待")
                    GPInfo("当前状态：第" + str(temp_shf + 1) + "个省份")
                    time.sleep(20)
                for temp_yy in range(len(hostipal[0])):
                    hostipalName = hostipal[0][temp_yy]  # 医院名
                    hostipalUrl = hostipal[1][temp_yy]  # 医院链接
                    finalInfo = {'省份名': shfName,
                                 '城市名': chsName,
                                 '医院名': hostipalName,
                                 '医院Url': hostipalUrl
                                 }
                    writer.writerow(finalInfo)


def savedoctorList(startnum, endnum, idnum):
    errornum = 0
    erroract = 0
    sum = 0

    with open("./data/ALLHostipalUrl.csv", newline='', encoding='utf-8') as f:
        data = list(csv.reader(f))
    with open("./data/ALLDoctorUrl" + str(idnum) + ".csv", 'w', newline='', encoding='utf-8')as ff:
        writer = csv.DictWriter(ff, key1)
        writer.writeheader()
        driver = initDriver(proxy.findapi())
        for i in range(startnum, int(endnum) + 1):
            if sum % 10 == 9:
                driver.quit()
                driver = initDriver(proxy.findProxy())
                GPAct("更换浏览器")
            try:
                url = doctorUrlList(data[i][3], driver)
                time.sleep(1)  # 等待数据处理
            except:
                continue
            for ii in url:
                try:
                    if sum % 10 == 9:
                        driver.quit()
                        driver = initDriver(proxy.findProxy())
                        GPAct("更换浏览器")
                    url = doctorUrlList(data[i][3], driver)
                    doctorUrl = doctorList(ii, driver)
                    time.sleep(1)  # 等待数据处理
                    erroract = 0
                except:
                    with open("./data/ErrorALLDoctorUrl.csv", 'w', newline='', encoding='utf-8')as fff:
                        finalInfo = {'省份名': data[i][0],
                                     '城市名': data[i][1],
                                     '医院名': data[i][2],
                                     '医院Url': ii
                                     }
                        Ewriter = csv.DictWriter(fff, key0)
                        Ewriter.writerow(finalInfo)
                        Ewriter.writeheader()
                        errornum += 1
                        erroract += 1
                        proxy.error()
                        # GPError("999", traceback.format_exc())
                    continue
                for iii in doctorUrl:
                    finalInfo = {'省份名': data[i][0],
                                 '城市名': data[i][1],
                                 '医院名': data[i][2],
                                 '医生Url': iii,
                                 '医生ID': sum
                                 }
                    sum += 1
                    writer.writerow(finalInfo)
            GPInfo("当前爬取医院进度[共" + str(len(data)) + "]：" + str(i) + "|错误数：" + str(errornum) + "范围" + str(
                startnum) + "-" + str(endnum))


# 用于saveinfo函数的数据读取计数
def readerData2():
    with open("./data/ALLDoctorUrl.csv", newline='', encoding='utf-8') as f:
        data = list(csv.reader(f))
        GPInfo("总计数量为：" + str(len(data) - 1))
    return str(len(data))


def readerData1():
    with open("./data/ALLHostipalUrl.csv", newline='', encoding='utf-8') as f:
        data = list(csv.reader(f))
        GPInfo("总计数量为：" + str(len(data) - 1))
    return str(len(data))


sum = 0  # 抓取计数器


def saveinfo(startnum, endnum, idnum):  # idnum为指纹计数器 分配不同代理
    errornum = 0
    erroract = 0
    sum = 0  # 总评论计数器

    global sumCPU  # 更换idnum

    # 可视化

    with logw.mode('医生评论数') as logger:
        conTag = logger.scalar('线程[' + str(idnum) + "]评论抓取" + str(startnum) + "-" + str(endnum))
    with logw.mode('抓取错误数') as logger:
        errorTag = logger.scalar('线程[' + str(idnum) + "]评论抓取" + str(startnum) + "-" + str(endnum))

    # 读取文件
    with open("./data/ALLDoctorUrl.csv", newline='', encoding='utf-8') as f:
        data = list(csv.reader(f))
    timea = str(timeinfo())  # 获取时间方便文件命名
    with open("./data/" + timea + "-" + str(idnum) + ".csv", 'w', newline='', encoding='utf-8')as ff:
        writer = csv.DictWriter(ff, key2)
        writer.writeheader()
        driver = initDriver(proxy.findapi())
        for i in range(startnum, endnum + 1):
            sumOnly = 0  # 单医生评论计数器
            if i % 20 == 19:
                driver.quit()
                driver = initDriver(proxy.findProxy())
                GPAct("更换浏览器")
            if erroract % 3 == 2:
                GPError("200", "被发现了，暂停3分钟")
                time.sleep(180)
            try:
                info = doctorinfo(data[i][3], driver=driver)  # 导入医生链接
                time.sleep(5)  # 等待数据处理
                erroract = 0
            except:
                with open("./data/Error" + timea + "-" + str(idnum) + ".csv", 'w', newline='', encoding='utf-8')as fff:
                    finalInfo = {'省份名': data[i][0],
                                 '城市名': data[i][1],
                                 '医院名': data[i][2],
                                 '医生Url': data[i][3],
                                 '医生ID': data[i][4]
                                 }
                    Ewriter = csv.DictWriter(fff, key1)
                    Ewriter.writerow(finalInfo)
                    errornum += 1
                    errorTag.add_record(i, errornum)  # 输入可视化数据
                    sumCPU += 1
                    proxy.error()
                    GPError("999", traceback.format_exc())
                continue
            try:
                for ii in range(len(info)):
                    finalInfo = {
                        '医生ID': data[i][4],

                        '省份名': data[i][0],
                        '城市名': data[i][1],
                        '医院名': data[i][2],
                        '医生姓名': info[ii][0],
                        '科室': info[ii][1],

                        '职称': info[ii][2],
                        '擅长': info[ii][3],
                        '经历': info[ii][4],
                        '疗效满意度': info[ii][5],
                        '态度满意度': info[ii][6],
                        '累计帮助患者数': info[ii][7],

                        '近两周帮助患者数': info[ii][8],
                        '临床经验统计': info[ii][9],
                        '治疗人数': info[ii][10],
                        '随访人数': info[ii][11],
                        '感谢信': info[ii][12],

                        '礼物数量': info[ii][13],
                        '服务星级': info[ii][14],
                        '值班': info[ii][15],
                        '出诊提示': info[ii][16],
                        '患者姓名': info[ii][17],
                        '症状': info[ii][18],

                        '看病目的': info[ii][19],
                        '治疗手段': info[ii][20],
                        '主观疗效': info[ii][21],
                        '态度': info[ii][22],
                        '感谢信&看病经验': info[ii][23],

                        '评价内容': info[ii][24],
                        '就诊理由': info[ii][25],
                        '挂号途径': info[ii][26],
                        '当前情况': info[ii][27],
                        '花费': info[ii][28],

                        '投票': info[ii][29],
                        '评论时间': info[ii][30],
                        '主页浏览量': info[ii][31],
                        '咨询信息列表': info[ii][32],
                        '照片': info[ii][33],
                        '推荐热度': info[ii][34]

                    }

                    sumOnly += 1
                    writer.writerow(finalInfo)
                sum += sumOnly
                conTag.add_record(i, sumOnly)  # 单医生评论量可视化
                allTag.add_record(idnum, sum)  # 线程总评论量可视化
                allErrorTag.add_record(idnum, errornum)  # 线程总错误
            except:
                errornum += 1
                GPError(202, "数据不完整")
                proxy.error()
                continue

            if i % 5 == 0:
                GPInfo("当前爬取医生进度[共" + str(len(data)) + "]：" + str(i) + "|错误数：" + str(errornum) + "|写入量" + str(sum))



# 多线程模块
sumCPU = 1  # 指纹、线程计数器[0-24]


def Threads_doctorUrl(startnum, endnum):
    threads = []
    readerData1()  # 获取数量
    num = input("请输入线程数[1-25]:")
    global sumCPU
    lang = (int(endnum) - int(startnum)) // int(num)
    tempstartnum = startnum
    tempendnum = startnum + lang
    for i in range(1, int(num) + 1):
        if i == int(num):
            cpu = threading.Thread(target=savedoctorList, args=(tempstartnum, endnum, sumCPU))
        else:
            cpu = threading.Thread(target=savedoctorList, args=(tempstartnum, tempendnum, sumCPU))
        tempstartnum += lang
        tempendnum += lang
        sumCPU += 1
        threads.append(cpu)
        GPInfo("线程" + str(i) + "准备完毕！")
    ii = 1
    for i in threads:
        i.start()
        GPInfo("线程" + str(ii) + "启动完毕！")
        ii += 1
        time.sleep(15)  # 错峰启动


def Threads_save(startnum, endnum):
    threads = []
    readerData2()  # 获取数量

    num = input("请输入线程数[1-25]:")
    global sumCPU
    # 起始位置
    lang = (int(endnum) - int(startnum)) // int(num)
    tempstartnum = startnum
    tempendnum = startnum + lang

    # 分配线程任务
    for i in range(1, int(num) + 1):
        if i == int(num):
            cpu = threading.Thread(target=saveinfo, args=(tempstartnum, endnum, sumCPU))
        else:
            cpu = threading.Thread(target=saveinfo, args=(tempstartnum, tempendnum, sumCPU))
        tempstartnum += lang
        tempendnum += lang
        sumCPU += 1
        threads.append(cpu)
        GPInfo("线程" + str(i) + "准备完毕！")
    ii = 1
    for i in threads:
        i.start()
        GPInfo("线程" + str(ii) + "启动完毕！")
        ii += 1
        time.sleep(30)  # 错峰启动


# 运行区
# savehostipalList()

# 信息表
starnum = int(input("输入开始位置_"))
endnum = int(input("输入结束位置_")) - 1
Threads_save(starnum, int(endnum))

'''
# 医生表
starnum = int(input("输入开始位置_"))
endnum = int(input("输入结束位置_")) - 1
Threads_doctorUrl(starnum, int(endnum))
'''
