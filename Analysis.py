import os

def is_num_by_except(num):
    try:
        int(num)
        return True
    except ValueError:
#        print "%s ValueError" % num
        return False

def data2class(data):
    classes = []
    for each in data:
        one = each.strip().split(":")
        classes.append(one)

    return classes


class AnalyWorker:
    data = [
        "48081:b01",
        "48153:B03",
        "48303:B01",
        "48182:B02",
        "48273:B01",
]
    targetClasses = set()
    targetClassesChanged = False
    rootPath = "/Users/Nathan/Desktop/"
    sourceTxt = "source.txt"
    htmlStr = "classHtmlStr.txt"
    command = "html2result"

    # 上一次运算的总表
    listenResult = []

    """
    参数是html返回的text
    """
    def __init__(self):
        self.data = data2class(self.data)


    """
    根据本地已存的旧的课程文件判断录入数据是否出错
    """
    def addListen(self,classid,roomid):
        if(len(roomid) != 3):
            return "errorTarget"

        if((classid+":"+roomid) in self.targetClasses):
            return "hasTarget"

        os.system("cd /Users/Nathan/Desktop")
        r = os.popen("/Users/Nathan/Desktop/html2result" + " " + classid + " " + roomid + " " + self.rootPath+self.sourceTxt).read().strip()
        t = r.split(sep="\n")
        if(len(t) != 2 or not is_num_by_except(t[0]) or not is_num_by_except(t[1])):
            return "errorTarget"

        self.targetClasses.add(classid+":"+roomid)
        self.targetClassesChanged = True
        return 0

    """
    根据更新后的文件运算结果
    [
        [实选数,可选人数,空位数,是否有空位,课程号,班号],
        [实选数,可选人数,空位数,是否有空位,课程号,班号],
        [实选数,可选人数,空位数,是否有空位,课程号,班号],
        [实选数,可选人数,空位数,是否有空位,课程号,班号],
        [实选数,可选人数,空位数,是否有空位,课程号,班号],
        [实选数,可选人数,空位数,是否有空位,课程号,班号],
        [实选数,可选人数,空位数,是否有空位,课程号,班号],
                        ....
    ]

    没有实现消息机制,所以所谓的新添加数据交集查询不会起作用(一个程序在循环里只能添加一次数据)
    """
    def computeResult(self):
        try:
            # 这一次运算后得到的总表
            tmpTotalResult = []
            for eachTarget in self.targetClasses:
                target = eachTarget.split(":")
                classid = target[0]
                roomid = target[1]


                commamdWithPath = self.rootPath+self.command
                targetFile = self.rootPath+self.htmlStr
                onceResult = os.popen(commamdWithPath + " " + classid + " " + roomid + " " + targetFile).read().strip().split("\n")
                onceResult[0] = int(onceResult[0])
                onceResult[1] = int(onceResult[1])
                if(onceResult[1] == 0):
                    onceResult.append(999)
                else:
                    onceResult.append( onceResult[1] - onceResult[0])
                    if(onceResult[2] > 0):
                        onceResult.append('T')
                    else:
                        onceResult.append('F')
                    onceResult.append(classid)
                    onceResult.append(roomid)
                tmpTotalResult.append(onceResult)



            # 相比于上次添加了的数据
            newListens = []
            # 本次要推送的数据
            sendResult = []
            # 新监听名单中的元素在上一次监听名单中
            inOld = False



            # 对于每一份需要被监听的课程
            for eachlatestResult in tmpTotalResult:
                # 和上一次的结果对比
                for each in self.listenResult:
                    if(eachlatestResult[4] == each[4] and eachlatestResult[5] == each[5]):
                        inOld = True
                        # 可选状态变化
                        if(each[3] != eachlatestResult[3]):
                            sendResult.append(eachlatestResult)
                        # 可选状态没有发生变化,但是都是可选并且还剩名额发生变化
                        elif(eachlatestResult[3] == 'T' and eachlatestResult[2] != each[2]):
                            sendResult.append(eachlatestResult)
                # 如果不在上一个名单里就再次考核
                if(inOld == False):
                    newListens.append(eachlatestResult)
                inOld = False

            for each in newListens:
                if each[3] == 'T':
                    sendResult.append(each)

            # 从sendResult截取需要的元素
            returnResult = []
            for each in sendResult:
                returnResult.append([each[4],each[5],each[2]])

            # 把当此的总结果设置成上次的总结过
            self.listenResult = tmpTotalResult

            return returnResult
        except Exception as e:
            print(str(e))
            print(onceResult)
