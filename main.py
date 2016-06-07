from Req import *
import time
from Analysis import *
import mail


if __name__ == '__main__':
    starttime = time.time()
    myss = mySession()
    myss.getCodeImage()
    code = input()
    myss.login(code)
    counter = 0
    myworker = AnalyWorker()
    for each in myworker.data:
        myworker.addListen(each[0],each[1])
    while(True):
        try:
            time.sleep(10)
            myss.findTargetStr()
            r = myworker.computeResult()
            if(len(r)>0):
                mailContent = ""
                for each in r:
                    mailContent += "课程号:" + str(each[0]) +"班级号:" + str(each[1]) + "可选人数:" + str(each[2]) +"\n"

                mailContent += time.strftime('%Y-%m-%d %H:%M:%S')
                mail.send_mail(mail.mailto_list,"选课变动提醒[不准很正常-.-]..退订联系我",mailContent)
            counter+=1


            with open("/Users/Nathan/Desktop/log.txt",'a') as f:
                print("共执行了:",counter,"次",time.time()-starttime, "秒",file=f)
        except Exception as e:
            print(str(e))
            mail.send_mail([767015792@qq.com],'Error',str(e))


