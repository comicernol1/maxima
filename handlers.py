import os,base64,tornado.web,urllib.parse,mysql.connector,smtplib
from cryptography.fernet import Fernet
Enc32a = Fernet(base64.b64encode(os.environ["Enc32a"].encode()))
Enc32b = Fernet(base64.b64encode(os.environ["Enc32b"].encode()))
db = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="maxima",
    password=str(os.environ["MYSQL_MAXIMA_PASSWD"]),
    database="franzar"
)
mycursor = db.cursor()

# Don't forget to eventually close the MySQL connection

class HomeHand(tornado.web.RequestHandler):
    def get(self):
        HomeProductList=""
        for i in range(0,1):
            HomeProductList+="<a href=\"/product/"+str(i)+"/\"><div class=\"BPX\"><span><abbr></abbr></span><h6>Product "+str(i)+"</h6><h1>$18.00</h1></div></a>\n"
        with open("/root/maxima/req/index.html") as HomeIndex_F:
                HomeIndex=HomeIndex_F.read()
        HomeIndex = HomeIndex.replace("<% Products %>", HomeProductList)
        
        self.set_status(200)
        self.set_header("Content-Type", "text/html")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header("Access-Control-Max-Age", 1000)
        self.set_header("Access-Control-Allow-Headers", "*")
        self.write(HomeIndex)

class SignInHand(tornado.web.RequestHandler):
    def get(self):
        with open("/root/maxima/req/sign_in/index.html") as SignInIndex_F:
                SignInIndex=SignInIndex_F.read()
        SignInIndex = SignInIndex.replace("<% ShowError %>","none")
        SignInIndex = SignInIndex.replace("<% ErrorMsg %>","")
        
        self.set_status(200)
        self.set_header("Content-Type", "text/html")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header("Access-Control-Max-Age", 1000)
        self.set_header("Access-Control-Allow-Headers", "*")
        self.write(SignInIndex)

    def post(self):
        SignInRequestBody=self.request.body.decode('utf-8')
        SignInRequestEmail=urllib.parse.unquote(SignInRequestBody[(SignInRequestBody.index("siem=")+5):SignInRequestBody.index("&sipw=")])
        SignInRequestPasswordPre=urllib.parse.unquote(SignInRequestBody[(SignInRequestBody.index("sipw=")+5):len(SignInRequestBody)])
        SignInRequestPassword=ph.hash(SignInRequestPasswordPre)
        SignInRequestDBInsert="INSERT INTO compacc (email, passwd) VALUES ('{0:s}', '{1:s}')".format(SignInRequestEmail, SignInRequestPassword)
        mycursor.execute(SignInRequestDBInsert)
        db.commit()

class SignUpHand(tornado.web.RequestHandler):
    def get(self):
        with open("/root/maxima/req/sign_up/index.html") as SignUpIndex_F:
                SignUpIndex=SignUpIndex_F.read()
        SignUpIndex = SignUpIndex.replace("<% ShowError %>","none")
        SignUpIndex = SignUpIndex.replace("<% ErrorMsg %>","")
        
        self.set_status(200)
        self.set_header("Content-Type", "text/html")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header("Access-Control-Max-Age", 1000)
        self.set_header("Access-Control-Allow-Headers", "*")
        self.write(SignUpIndex)

    def post(self):
        with open("/root/maxima/req/sign_up/index.html") as SignUpIndex_F:
                SignUpIndex=SignUpIndex_F.read()
        with open("/root/maxima/req/sign_in/index.html") as SignInIndex_F:
                SignInIndex=SignInIndex_F.read()
        
        SignUpRequestBody=self.request.body.decode('utf-8')
        SignUpRequestEmail=urllib.parse.unquote(SignUpRequestBody[(SignUpRequestBody.index("suem=")+5):SignUpRequestBody.index("&supw=")])
        SignUpRequestDBSelectEmail="SELECT COUNT(*) from compacc where email='{0:s}'".format(SignUpRequestEmail)
        mycursor.execute(SignUpRequestDBSelectEmail)
        QueryCountEmail=mycursor.fetchone()
        SignUpRequestPasswordPre=urllib.parse.unquote(SignUpRequestBody[(SignUpRequestBody.index("supw=")+5):SignUpRequestBody.index("&supa=")])
        SignUpRequestPassword=Enc32a.encrypt(SignUpRequestPasswordPre.encode()).decode('utf-8')
        SignUpRequestPasswordAgain=urllib.parse.unquote(SignUpRequestBody[(SignUpRequestBody.index("supa=")+5):len(SignUpRequestBody)])
        if len(SignUpRequestPasswordPre)>=8 and SignUpRequestPasswordPre==SignUpRequestPasswordAgain and int(QueryCountEmail[0])<1:
            SignUpRequestDBInsert="INSERT INTO compacc (email, passwd) VALUES ('{0:s}', '{1:s}')".format(SignUpRequestEmail, SignUpRequestPassword)
            mycursor.execute(SignUpRequestDBInsert)
            db.commit()
            with open("/root/maxima/templates/sign_up/conf_email.html") as SignUpSMPTTemplate_F:
                SignUpSMTPTemplate=SignUpSMPTTemplate_F.read()
            SignUpSMTPHeaders="\r\n".join(["from: comicernol@gmail.com","subject: Verify Your Email - FRANZAR","to:"+SignUpRequestEmail,"mime-version: 1.0","content-type: text/html"])
            SignUpSMTPContent=SignUpSMTPHeaders+"\r\n\r\n"+SignUpSMTPTemplate
            SignUpMail=smtplib.SMTP('smtp.gmail.com',587)
            SignUpMail.ehlo()
            SignUpMail.starttls()
            SignUpMail.login('comicernol@gmail.com',str(os.environ["Comicernol_Gmail_Passwd"]))
            SignUpMail.sendmail('comicernol@gmail.com',SignUpRequestEmail,SignUpSMTPContent)
            SignUpMail.close()
            self.render('sign_up/conf_sent.html')
        elif int(QueryCountEmail[0])>=1:
            SignInIndex = SignInIndex.replace("<% ShowError %>","block")
            SignInIndex = SignInIndex.replace("<% ErrorMsg %>","Your account already exists.")
            self.write(SignInIndex)
        else:
            SignUpIndex = SignUpIndex.replace("<% ShowError %>","block")
            SignUpIndex = SignUpIndex.replace("<% ErrorMsg %>","Something went wrong, please try again")
            self.render(SignUpIndex)
