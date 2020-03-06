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
        self.set_status(200)
        self.set_header("Content-Type", "text/html")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header("Access-Control-Max-Age", 1000)
        self.set_header("Access-Control-Allow-Headers", "*")
        self.render('index.html')

class SignInHand(tornado.web.RequestHandler):
    def get(self):
        self.set_status(200)
        self.set_header("Content-Type", "text/html")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header("Access-Control-Max-Age", 1000)
        self.set_header("Access-Control-Allow-Headers", "*")
        self.render('sign_in.html')

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
        self.set_status(200)
        self.set_header("Content-Type", "text/html")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header("Access-Control-Max-Age", 1000)
        self.set_header("Access-Control-Allow-Headers", "*")
        self.render('sign_up.html')

    def post(self):
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
            SignUpSMTPTemplate="<center><h1>Please click here to verify your email address:</h1><br><a href=\"http://www.kelimart.com/verify/?e=stuff\">Click Here</a></center>"
            SignUpSMTPHeaders="\r\n".join(["from: comicernol@gmail.com","subject: Testing","to:"+SignUpRequestEmail,"mime-version: 1.0","content-type: text/html"])
            SignUpSMTPContent=SignUpSMTPHeaders+"\r\n\r\n"+SignUpSMTPTemplate
            SignUpMail=smtplib.SMTP('smtp.gmail.com',587)
            SignUpMail.ehlo()
            SignUpMail.starttls()
            SignUpMail.login('comicernol@gmail.com',str(os.environ["Comicernol_Gmail_Passwd"]))
            SignUpMail.sendmail('comicernol@gmail.com',SignUpRequestEmail,SignUpSMTPContent)
            SignUpMail.close()
            
