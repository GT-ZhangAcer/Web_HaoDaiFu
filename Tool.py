import sys

def GPInfo(info):
    print("INFO:",info)

def GPError(num,info):
    print("===ERROR===",num,':',info)

def GPAct(info):
    print("ACT:",info,"ing...")


def workPath():
    ScriptFilePath=(sys.argv[0])#获得的是当前执行脚本的位置（若在命令行执行的该命令，则为空）
    try:
        WorkPathNum=ScriptFilePath.rindex('/')
    except:
        WorkPathNum = ScriptFilePath.rindex('\\')
    WorkPath=ScriptFilePath[0:WorkPathNum+1]#切片
    print("当前工作目录为："+WorkPath)
    return  WorkPath