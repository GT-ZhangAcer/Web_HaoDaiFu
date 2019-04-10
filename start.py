from MainScript import *
import threading

key0 = ['省份名', '城市名', '医院名', '医院Url']  # 数据表头 0-3
key1 = ['省份名', '城市名', '医院名', '医生Url']  # 数据表头 0-3
key2 = ['省份名', '城市名', '医院名', '医生姓名',  # 3+1
        '科室', '职称', '擅长', '经历', '疗效满意度',  # 5
        '态度满意度', '累计帮助患者数', '近两周帮助患者数',  # 3
        '临床经验统计', '治疗人数', '随访人数', '感谢信', '礼物数量', '服务星级',  # 6
        '值班', '出诊提示', '患者姓名', '症状', '看病目的',  # 5
        '治疗手段', '主观疗效', '感谢信&看病经验', '态度', '评价内容', '就诊理由', '挂号途径', '当前情况',  # 8
        '花费', '投票', '主页浏览量', '咨询信息列表','照片','推荐热度']  # 5 数据表头 0-3-32


def savehostipalList():
    csvName = "./data/ALLHostipalUrl" + str(timeinfo()) + ".csv"
    with open(csvName, 'w', newline='', encoding='utf-8') as f:  # 数据准备写入
        writer = csv.DictWriter(f, key0)
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
    with open("./data/ALLDoctorUrl."+str(idnum)+"csv", 'w', newline='', encoding='utf-8')as ff:
        writer = csv.DictWriter(ff, key1)
        writer.writeheader()
        for i in range(startnum, int(endnum)):
            url = doctorUrlList(data[i][3])
            for ii in url:
                if erroract % 3 == 2:

                    GPError("200", "被发现了，暂停3分钟")
                    time.sleep(180)
                try:
                    doctorUrl = doctorList(ii,idnum)
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
                        GPError("999", traceback.format_exc())
                        idnum=idnum%10+9#换代理
                    continue
                time.sleep(10 + erroract)
                for iii in doctorUrl:
                    finalInfo = {'省份名': data[i][0],
                                 '城市名': data[i][1],
                                 '医院名': data[i][2],
                                 '医生Url': iii
                                 }
                    sum += 1
                    writer.writerow(finalInfo)
                GPInfo("当前爬取医院进度[共" + str(len(data)) + "]：" + str(i) + "|错误数：" + str(errornum) + "|写入量" + str(sum))


# 用于saveinfo函数的数据读取计数
def readerData2():
    with open("./data/ALLDoctorUrl.csv", newline='', encoding='utf-8') as f:
        data = list(csv.reader(f))
        GPInfo("总计数量为：" + str(len(data)))
    return str(len(data))


def readerData1():
    with open("./data/ALLHostipalUrl.csv", newline='', encoding='utf-8') as f:
        data = list(csv.reader(f))
        GPInfo("总计数量为：" + str(len(data)))
    return str(len(data))


sum = 0#抓取计数器


def saveinfo(startnum, endnum, idnum):  # idnum为指纹计数器 分配不同代理
    errornum = 0
    erroract = 0
    global sum
    global sumCPU#更换idnum
    with open("./data/ALLDoctorUrl.csv", newline='', encoding='utf-8') as f:
        data = list(csv.reader(f))
    timea = str(timeinfo())  # 获取时间方便文件命名
    with open("./data/" + timea + "-" + str(idnum) + ".csv", 'w', newline='', encoding='utf-8')as ff:
        writer = csv.DictWriter(ff, key2)
        writer.writeheader()
        driver = initDriver(idnum)
        try:
            if str(driver) == "1":
                sumCPU += 1
        except:
            pass
        for i in range(startnum, endnum):
            if i % 20 == 19:
                driver.quit()
                driver = initDriver(sumCPU)
                GPAct("更换浏览器")
            if erroract % 3 == 2:
                GPError("200", "被发现了，暂停3分钟")
                time.sleep(180)
            try:
                info = doctorinfo(data[i][3], driver=driver)
                erroract = 0
            except:
                with open("./data/Error" + timea + "-" + str(idnum) + ".csv", 'w', newline='', encoding='utf-8')as fff:
                    finalInfo = {'省份名': data[i][0],
                                 '城市名': data[i][1],
                                 '医院名': data[i][2],
                                 '医生Url': data[i][3]
                                 }
                    Ewriter = csv.DictWriter(fff, key1)
                    Ewriter.writerow(finalInfo)
                    errornum += 1
                    sumCPU += 1
                continue
            try:
                for ii in range(len(info)):
                    finalInfo = {'省份名': data[i][0],
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
                                 '主页浏览量': info[ii][30],
                                 '咨询信息列表':info[ii][31],
                                 '照片':info[ii][32],
                                 '推荐热度': info[ii][33]

                                 }

                    sum += 1
                    writer.writerow(finalInfo)

            except:
                errornum += 1
                GPError(202, "数据不完整")
                continue
            '''
            if i % 5 == 0:
                GPInfo("当前爬取医生进度[共" + str(len(data)) + "]：" + str(i) + "|错误数：" + str(errornum) + "|写入量" + str(sum))
            '''


# 多线程模块
sumCPU = 1  # 指纹、线程计数器[0-24]


def Threads_doctorUrl(startnum, endnum):
    threads = []
    readerData1()  # 获取数量
    num = input("请输入线程数[1-25]:")
    global sumCPU
    lang = (int(endnum) - int(startnum)) // int(num)
    tempstartnum = 1
    tempendnum = 1 + lang
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


def Threads_save(startnum, endnum):
    threads = []
    readerData2()  # 获取数量
    num = input("请输入线程数[1-25]:")
    global sumCPU
    # 起始位置
    lang = (int(endnum) - int(startnum)) // int(num)
    tempstartnum = 1
    tempendnum = 1 + lang

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
        time.sleep(15)  # 错峰启动


# savehostipalList()
# savedoctorList(1)


# saveinfo(1,5,1)
"""
运行区
"""
'''
#信息表
endnum = input("输入结束位置_")
print(timeinfo())
Threads_save(1, int(endnum) + 1)
'''

#医生表
endnum = input("输入结束位置_")
Threads_doctorUrl(1, int(endnum) + 1)
