import sys
import time


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
        'Mozilla/4.0 (compatible; MSIE  7.0; Windows NT 5.1; 360SE)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)']
    return list[int]


def strClean(str1):
    str1 = str(str1).replace(" ", '').replace("\n", "").replace("\t", '').replace("\\n", "").replace("\\t", "").replace(
        "&nbsp", "").replace("\\xa0", "").replace("\xa0", "").replace("\\", '')#怎么说呢 太诡异了
    return str1


def timeinfo():
    timea = time.strftime("%Y-%m-%d-%H-%M", time.localtime())  # 获取当前时间
    return timea
