import os,random,base64,tornado.web,urllib.parse,mysql.connector,smtplib
from cryptography.fernet import Fernet
Enc32a = Fernet(base64.b64encode(os.environ["Enc32a"].encode()))
Enc32b = Fernet(base64.b64encode(os.environ["Enc32b"].encode()))
db = mysql.connector.connect(
    host = "127.0.0.1",
    port = 3306,
    user = "maxima",
    password = str(os.environ["MYSQL_MAXIMA_PASSWD"]),
    database = "franzar"
)
mycursor = db.cursor()

# Don't forget to eventually close the MySQL connection

class HomeHand(tornado.web.RequestHandler):
    def get(self):
        HomeProductList = ""
        for i in range(0,1):
            HomeProductList += "<a href=\"/product/"+str(i)+"/\"><div class=\"BPX\"><span><abbr></abbr></span><h6>Product "+str(i)+"</h6><h1>$18.00</h1></div></a>\n"
        with open("/root/maxima/req/index.html") as HomeIndex_F:
            HomeIndex = HomeIndex_F.read()
        HomeIndex = HomeIndex.replace("<% Products %>", HomeProductList)
        if self.get_secure_cookie("Fu") and self.get_secure_cookie("Ft"):
            UserInfoFu = self.get_secure_cookie("Fu")
            UserInfoFt = self.get_secure_cookie("Ft")
            UserInfoLoginQuery = "SELECT * from compacc where userid='{0:d}' and token='{1:d}'".format(int(UserInfoFu),int(UserInfoFt))
            mycursor.execute(UserInfoLoginQuery)
            UserInfoLoginFetch = mycursor.fetchone()
            HeaderLIPre = "<li><a href=\"/\"><b>Home</b></a></li><li><a href=\"/contact/\">Contact</a></li>"
            if UserInfoLoginFetch:
                HomeIndex = HomeIndex.replace("<% HeaderLI %>",HeaderLIPre+"<li id=\"HMs\"><a href=\"/account/\">My Account</a><span></span></li>")
            else:
                HomeIndex = HomeIndex.replace("<% HeaderLI %>",HeaderLIPre+"<li id=\"HMs\"><a href=\"/sign_in/\">Sign In</a></li>")
        else:
            HomeIndex = HomeIndex.replace("<% HeaderLI %>",HeaderLIPre+"<li id=\"HMs\"><a href=\"/sign_in/\">Sign In</a></li>")
        HomeIndex = HomeIndex.replace("<% Head %>","<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"><meta name=\"apple-mobile-web-app-title\" content=\"Franzar\" /><meta name=\"description\" content=\"\"><meta name=\"keywords\" content=\"Franzar, Franzar.com\"><link rel=\"canonical\" href=\"https://www.franzar.com/\"><link rel=\"icon\" href=\"/static/favicon32.png\" sizes=\"32x32\"><link rel=\"icon\" href=\"/static/favicon192.png\" sizes=\"192x192\"><link rel=\"apple-touch-icon\" href=\"/static/favicon180.png\" sizes=\"180x180\"><meta name=\"msapplication-TileImage\" content=\"/static/favicon32.png\"><meta name=\"msapplication-TileColor\" content=\"#FFFFFF\"><meta name=\"theme-color\" content=\"\"><link rel=\"shortcut icon\" href=\"/static/favicon64.png\"><link rel=\"preload\" href=\"/static/multiplier_image.png\" as=\"image\">")
        with open("/root/maxima/templates/footer.html") as FooterHTML_F:
            FooterHTML = FooterHTML_F.read()
        HomeIndex = HomeIndex.replace("<% Footer %>",FooterHTML)
        
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
            SignInIndex = SignInIndex_F.read()
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
        with open("/root/maxima/req/sign_up/index.html") as SignUpIndex_F:
            SignUpIndex = SignUpIndex_F.read()
        with open("/root/maxima/req/sign_in/index.html") as SignInIndex_F:
            SignInIndex = SignInIndex_F.read()
        SignInRequestBody = self.request.body.decode('utf-8')
        if SignInRequestBody.find("siem=") >= 0 and SignInRequestBody.find("sipw=") >= 0:
            SignInRequestEmail = urllib.parse.unquote(SignInRequestBody[(SignInRequestBody.index("siem=")+5):SignInRequestBody.index("&sipw=")])
            SignInRequestPassword = urllib.parse.unquote(SignInRequestBody[(SignInRequestBody.index("sipw=")+5):len(SignInRequestBody)])
            SignInRequestDBSelectEmail = "SELECT passwd,userid from compacc where email='{0:s}'".format(SignInRequestEmail)
            mycursor.execute(SignInRequestDBSelectEmail)
            QueryEmailPre = mycursor.fetchone()
            if QueryEmailPre:
                QueryEmailPw = QueryEmailPre[0].encode()
                QueryEmailUserID = str(QueryEmailPre[1])
                SignInQueryPassword = Enc32a.decrypt(QueryEmailPw).decode('utf-8')
                if SignInQueryPassword == SignInRequestPassword:
                    SignInRequestToken = random.randint(1000000000,9999999999)
                    SignInRequestDBUpdate = "UPDATE compacc SET token='{0:d}' WHERE email='{1:s}'".format(SignInRequestToken,SignInRequestEmail)
                    mycursor.execute(SignInRequestDBUpdate)
                    db.commit()
                    self.set_secure_cookie("Fu",QueryEmailUserID)
                    self.set_secure_cookie("Ft",str(SignInRequestToken))
                    self.redirect("/")
                else:
                    SignInIndex = SignInIndex.replace("<% ShowError %>","block")
                    SignInIndex = SignInIndex.replace("<% ErrorMsg %>","Incorrect Password")
                    self.write(SignInIndex)
            else:
                SignInIndex = SignInIndex.replace("<% ShowError %>","block")
                SignInIndex = SignInIndex.replace("<% ErrorMsg %>","Account already exists")
                self.write(SignInIndex)
        else:
            SignInIndex = SignInIndex.replace("<% ShowError %>","block")
            SignInIndex = SignInIndex.replace("<% ErrorMsg %>","(N1) Something went wrong, please try again")
            self.write(SignInIndex)

class SignUpHand(tornado.web.RequestHandler):
    def get(self):
        with open("/root/maxima/req/sign_up/index.html") as SignUpIndex_F:
            SignUpIndex = SignUpIndex_F.read()
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
            SignUpIndex = SignUpIndex_F.read()
        with open("/root/maxima/req/sign_up/conf_sent.html") as SignUpConf_F:
            SignUpConf = SignUpConf_F.read()
        with open("/root/maxima/req/sign_in/index.html") as SignInIndex_F:
            SignInIndex = SignInIndex_F.read()
        
        SignUpRequestBody = self.request.body.decode('utf-8')
        if SignUpRequestBody.find("suem=") >= 0 and SignUpRequestBody.find("supw=") >= 0 and SignUpRequestBody.find("supa=") >= 0:
            SignUpRequestEmail = urllib.parse.unquote(SignUpRequestBody[(SignUpRequestBody.index("suem=")+5):SignUpRequestBody.index("&supw=")])
            SignUpRequestDBSelectEmail = "SELECT COUNT(*) from compacc where email='{0:s}'".format(SignUpRequestEmail)
            mycursor.execute(SignUpRequestDBSelectEmail)
            QueryCountEmail = mycursor.fetchone()
            SignUpRequestPasswordPre = urllib.parse.unquote(SignUpRequestBody[(SignUpRequestBody.index("supw=")+5):SignUpRequestBody.index("&supa=")])
            SignUpRequestPassword = Enc32a.encrypt(SignUpRequestPasswordPre.encode()).decode('utf-8')
            SignUpRequestPasswordAgain = urllib.parse.unquote(SignUpRequestBody[(SignUpRequestBody.index("supa=")+5):len(SignUpRequestBody)])
            if SignUpRequestBody.find("rsve=y") and len(SignUpRequestPasswordPre) >= 8 and SignUpRequestPasswordPre == SignUpRequestPasswordAgain and int(QueryCountEmail[0]) < 1:
                SignUpVerifyCode = random.randint(1000000000,9999999999)
                SignUpRequestDBInsert = "INSERT INTO compacc (userid,email,veremail,passwd,token) VALUES ('{0:d}','{1:s}',0,'{2:s}','')".format(SignUpVerifyCode,SignUpRequestEmail,SignUpRequestPassword)
                mycursor.execute(SignUpRequestDBInsert)
                db.commit()
                with open("/root/maxima/templates/sign_up/conf_email.html") as SignUpSMPTTemplate_F:
                    SignUpSMTPTemplate = SignUpSMPTTemplate_F.read()
                SignUpSMTPTemplate = SignUpSMTPTemplate.replace("<% UserCode %>",str(SignUpVerifyCode))
                SignUpSMTPHeaders = "\r\n".join(["from: comicernol@gmail.com","subject: Verify Your Email - FRANZAR","to:"+SignUpRequestEmail,"mime-version: 1.0","content-type: text/html"])
                SignUpSMTPContent = SignUpSMTPHeaders+"\r\n\r\n"+SignUpSMTPTemplate
                SignUpMail = smtplib.SMTP('smtp.gmail.com',587)
                SignUpMail.ehlo()
                SignUpMail.starttls()
                SignUpMail.login('comicernol@gmail.com',str(os.environ["Comicernol_Gmail_Passwd"]))
                SignUpMail.sendmail('comicernol@gmail.com',SignUpRequestEmail,SignUpSMTPContent)
                SignUpMail.close()
                SignUpConf = SignUpConf.replace("<% Email %>",SignUpRequestEmail)
                self.write(SignUpConf)
            elif SignUpRequestBody.find("rsve=y") == -1 and int(QueryCountEmail[0]) >= 1:
                SignUpIndex = SignUpIndex.replace("<% ShowError %>","block")
                SignUpIndex = SignUpIndex.replace("<% ErrorMsg %>","This account already exists")
                self.write(SignUpIndex)
            else:
                SignUpIndex = SignUpIndex.replace("<% ShowError %>","block")
                SignUpIndex = SignUpIndex.replace("<% ErrorMsg %>","(P1) Something went wrong, please try again")
                self.write(SignUpIndex)
        elif SignUpRequestBody.find("rsve=") >= 0:
            SignUpRSVEEmail = urllib.parse.unquote(SignUpRequestBody[(SignUpRequestBody.index("rsve=")+5):len(SignUpRequestBody)])
            with open("/root/maxima/templates/sign_up/conf_email.html") as SignUpSMPTTemplate_F:
                    SignUpSMTPTemplate = SignUpSMPTTemplate_F.read()
            SignUpSMTPHeaders = "\r\n".join(["from: comicernol@gmail.com","subject: Verify Your Email - FRANZAR","to:"+SignUpRSVEEmail,"mime-version: 1.0","content-type: text/html"])
            SignUpSMTPContent = SignUpSMTPHeaders+"\r\n\r\n"+SignUpSMTPTemplate
            SignUpMail = smtplib.SMTP('smtp.gmail.com',587)
            SignUpMail.ehlo()
            SignUpMail.starttls()
            SignUpMail.login('comicernol@gmail.com',str(os.environ["Comicernol_Gmail_Passwd"]))
            SignUpMail.sendmail('comicernol@gmail.com',SignUpRSVEEmail,SignUpSMTPContent)
            SignUpMail.close()
            SignUpConf = SignUpConf.replace("<% Email %>",SignUpRSVEEmail)
            self.write(SignUpConf)
        else:
            SignUpIndex = SignUpIndex.replace("<% ShowError %>","block")
            SignUpIndex = SignUpIndex.replace("<% ErrorMsg %>","(P2) Something went wrong, please try again")
            self.write(SignUpIndex)
class VerifyHand(tornado.web.RequestHandler):
    def get(self):
        with open("/root/maxima/req/sign_up/verified.html") as VerifyIndex_F:
            VerifyIndex = VerifyIndex_F.read()
        VerifyIndex = VerifyIndex.replace("<% Email %>",self.get_query_argument("e"))
        
        self.set_status(200)
        self.set_header("Content-Type", "text/html")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header("Access-Control-Max-Age", 1000)
        self.set_header("Access-Control-Allow-Headers", "*")
        self.write(VerifyIndex)
