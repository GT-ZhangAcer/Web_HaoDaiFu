from MainScript import *

key0 = ['省份名', '城市名', '医院名', '医院Url']  # 数据表头 0-3
key1 = ['省份名', '城市名', '医院名', '医生url']  # 数据表头 0-3
key2 = ['省份名', '城市名', '医院名', '医生信息', '主观疗效', '态度', '评价内容', '花费']  # 数据表头 0-3-7


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
                                     'Url': hostipalUrl
                                     }
                        writer.writerow(finalInfo)


def savedoctorList():
    errornum=0
    with open("./data/ALLHostipalUrl.csv", 'w', newline='', encoding='utf-8') as f:
        data = csv.reader(f)
    with open("./data/ALLDoctorUrl.csv", 'w', newline='', encoding='utf-8')as ff:
        writer = csv.DictWriter(ff, key1)
        for i in range(1, len(data)):
            url = doctorUrlList(data[i][3])
            for ii in url:
                try:
                    doctorUrl = doctorList(ii)
                except:
                    with open("./data/ErrorALLDoctorUrl.csv", 'w', newline='', encoding='utf-8')as fff:
                        finalInfo = {'省份名': data[i][0],
                                     '城市名': data[i][1],
                                     '医院名': data[i][2],
                                     'Url': ii
                                     }
                        Ewriter = csv.DictWriter(fff, key0)
                        Ewriter.writerow(finalInfo)
                        errornum+=1
                    continue
                if ii % 10 == 0:
                    GPAct("防止反爬检测，暂停进行等待")
                    time.sleep(10)
                finalInfo = {'省份名': data[i][0],
                             '城市名': data[i][1],
                             '医院名': data[i][2],
                             'Url': doctorUrl
                             }
                writer.writerow(finalInfo)
                if ii % 100 == 0:
                    GPInfo("当前爬取医院进度[共8058]：" + str(i)+"|错误数："+str(errornum))


def saveinfo():
    errornum=0
    with open("./data/ALLDoctorUrl.csv", 'w', newline='', encoding='utf-8') as f:
        data = csv.reader(f)
    timea = str(timeinfo())
    with open("./data/" + timea + ".csv", 'w', newline='', encoding='utf-8')as ff:
        writer = csv.DictWriter(ff, key2)
        driver = initDriver()
        for i in range(1, len(data)):
            if i%20==0:
                driver.quit()
                driver=initDriver()
                GPAct("更换浏览器")
            try:
                info = doctorinfo(data[i][3], driver=driver)
            except:
                with open("./data/Error" + timea + ".csv", 'w', newline='', encoding='utf-8')as fff:
                    finalInfo = {'省份名': data[i][0],
                                 '城市名': data[i][1],
                                 '医院名': data[i][2],
                                 'Url': data[i][3]
                                 }
                    Ewriter = csv.DictWriter(fff, key0)
                    Ewriter.writerow(finalInfo)
                    errornum+=1
                continue

            finalInfo = {'省份名': data[i][0],
                         '城市名': data[i][1],
                         '医院名': data[i][2],
                         '医生信息': info[0],
                         '主观疗效': info[1],
                         '态度': info[2],
                         '评价内容': info[3],
                         '花费': info[4]}
            writer.writerow(finalInfo)
            if i % 100 == 0:
                GPInfo("当前爬取医生进度[共" + str(len(data)) + "]：" + str(i)+"|错误数："+str(errornum))

# savehostipalList()
