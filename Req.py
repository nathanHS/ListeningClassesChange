import requests

class mySession:

    hasSessionInClassList = False
    s = requests.Session()
    websit = 'http://portal.jxufe.edu.cn/'
    """
    获取验证码图片
    """
    def getCodeImage(self):
        r = self.s.get(self.websit+'codeimage', stream=True) # here we need to set stream = True parameter
        with open("/Users/Nathan/Desktop/codeImage.png", 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
            f.close()

    """
    通过账号登陆
    """
    def login(self,imagecode,id = '2201404085',key = 'keyword'):
        mydata = {
            'p_p_id':'58',
            'p_p_lifecycle':'1',
            'p_p_state':'normal',
            'p_p_mode':'view',
            'p_p_col_id':'column-1',
            'p_p_col_count':'1',
            'saveLastPath':'0',
            '_58_struts_action':"/login/login",
            'errors':'0',
            'imageCodeName':imagecode,
            '_58_login':id,
            'password':key
        }
        r = self.s.post(self.websit+"/web/guest/home",data=mydata)
        r = 1

    def findTargetStr(self):
        if(not self.hasSessionInClassList):
            r=self.s.get("http://xfz.jxufe.edu.cn/")
            r=self.s.get("http://xfz.jxufe.edu.cn/portal/main.xsp/page/-2")
            r=self.s.get("http://xfz.jxufe.edu.cn/portal/main.xsp/page/-2/?.a.p=aT0lMkZ4Znpwb3J0YWwlMkZpbmZvcjRBbGwmdD1yJnM9bm9ybWFsJmVzPWRldGFjaCZtPXZpZXc%3D&mlinkf=infor4All%2Findex4departmentall.jsp")

        self.hasSessionInClassList = True

        tmpdata = {
            "DepartmentCaption":"",
            "DepartmentCode":"",
            "departmentSelect":"%E9%83%A8%E9%97%A8",
            "term":"161"
        }

        r=self.s.post("http://xfz.jxufe.edu.cn/portal/main.xsp/page/-2/?.a.p=aT0lMkZ4Znpwb3J0YWwlMkZpbmZvcjRBbGwmdD1yJnM9bm9ybWFsJmVzPWRldGFjaCZtPXZpZXc%3D&mlinkf=infor4All%2Findex4departmentall.jsp",data=tmpdata)

        with open("/Users/Nathan/Desktop/classHtmlStr.txt",'w') as f:
            print(r.text,file=f)


