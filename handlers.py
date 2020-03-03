import os,tornado.web,urllib.parse,mysql.connector
from argon2 import PasswordHasher
ph = PasswordHasher()
db = mysql.connector.connect(
  host="localhost",
  user="maxima",
  passwd=str(os.environ["MYSQL_MAXIMA_PASSWD"]),
  database="franzar"
)
mycursor = db.cursor()

class HomeHand(tornado.web.RequestHandler):
  def get(self):
    if self.request.host=="kelimart.com" or self.request.host=="www.kelimart.com":
      self.set_status(200)
      self.set_header("Content-Type", "text/html")
      self.set_header("Access-Control-Allow-Origin", "*")
      self.set_header("Access-Control-Allow-Headers", "*")
      self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
      self.set_header("Access-Control-Max-Age", 1000)
      self.set_header("Access-Control-Allow-Headers", "*")
      self.render('index.html')
    else:
      self.set_status(404)

class SignInHand(tornado.web.RequestHandler):
  def get(self):
    if self.request.host=="kelimart.com" or self.request.host=="www.kelimart.com":
      self.set_status(200)
      self.set_header("Content-Type", "text/html")
      self.set_header("Access-Control-Allow-Origin", "*")
      self.set_header("Access-Control-Allow-Headers", "*")
      self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
      self.set_header("Access-Control-Max-Age", 1000)
      self.set_header("Access-Control-Allow-Headers", "*")
      self.render('signin.html')
    else:
      self.set_status(404)

    def post(self):
      if self.request.host=="kelimart.com" or self.request.host=="www.kelimart.com":
        SignInRequestBody=self.request.body.decode('utf-8')
        SignInRequestEmail=urllib.parse.unquote(SignInRequestBody[(SignInRequestBody.index("siem=")+5):SignInRequestBody.index("&sipw=")])
        
        SignInRequestPasswordPre=urllib.parse.unquote(SignInRequestBody[(SignInRequestBody.index("sipw=")+5):len(SignInRequestBody)])
        SignInRequestPassword=ph.hash(SignInRequestPasswordPre)
        SignInRequestDBInsert="INSERT INTO compacc (email, passwd) VALUES ('{0:s}', '{1:s}')".format(SignInRequestEmail, SignInRequestPassword)
        mycursor.execute(SignInRequestDBInsert)
        db.commit()
      else:
        self.set_status(404)

class SignUpHand(tornado.web.RequestHandler):
  def get(self):
    if self.request.host=="kelimart.com" or self.request.host=="www.kelimart.com":
      self.set_status(200)
      self.set_header("Content-Type", "text/html")
      self.set_header("Access-Control-Allow-Origin", "*")
      self.set_header("Access-Control-Allow-Headers", "*")
      self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
      self.set_header("Access-Control-Max-Age", 1000)
      self.set_header("Access-Control-Allow-Headers", "*")
      self.render('signup.html')
    else:
      self.set_status(404)

  def post(self):
    if self.request.host=="kelimart.com" or self.request.host=="www.kelimart.com":
      SignUpRequestBody=self.request.body.decode('utf-8')
      SignUpRequestEmail=urllib.parse.unquote(SignUpRequestBody[(SignUpRequestBody.index("suem=")+5):SignUpRequestBody.index("&supw=")])
        
      SignUpRequestPasswordPre=urllib.parse.unquote(SignUpRequestBody[(SignUpRequestBody.index("supw=")+5):len(SignUpRequestBody)])
      SignUpRequestPassword=ph.hash(SignUpRequestPasswordPre)
      SignUpRequestDBInsert="INSERT INTO compacc (email, passwd) VALUES ('{0:s}', '{1:s}')".format(SignUpRequestEmail, SignUpRequestPassword)
      mycursor.execute(SignUpRequestDBInsert)
      db.commit()
    else:
      self.set_status(404)

db.close()
