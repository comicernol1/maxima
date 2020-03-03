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
      self.render('index.html')

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
        SignInRequestBody=self.request.body.decode('utf-8')
        SignInRequestEmail=urllib.parse.unquote(SignInRequestBody[(SignInRequestBody.index("siem=")+5):SignInRequestBody.index("&sipw=")])
        
        SignInRequestPasswordPre=urllib.parse.unquote(SignInRequestBody[(SignInRequestBody.index("sipw=")+5):len(SignInRequestBody)])
        SignInRequestPassword=ph.hash(SignInRequestPasswordPre)
        SignInRequestDBInsert="INSERT INTO compacc (email, passwd) VALUES ('{0:s}', '{1:s}')".format(SignInRequestEmail, SignInRequestPassword)
        mycursor.execute(SignInRequestDBInsert)
        db.commit()

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

db.close()






class HomeHTMLHand(tornado.web.RequestHandler):
    def get(self):
        if self.request.host=="kelimart.com" or self.request.host=="www.kelimart.com":
            self.set_status(200)
            self.set_header("Content-Type", "text/html")
            self.set_header("Access-Control-Allow-Origin", "*")
            self.set_header("Access-Control-Allow-Headers", "*")
            self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
            self.set_header("Access-Control-Max-Age", 1000)
            self.set_header("Access-Control-Allow-Headers", "*")
            with open("/root/maxima/kelimart/index.html", "r") as kelimart_home_html:
                self.write(kelimart_home_html.read())
            kelimart_home_html.close()
        else:
            self.set_status(404)

class HomeCSSHand(tornado.web.RequestHandler):
    def get(self):
        if self.request.host=="kelimart.com" or self.request.host=="www.kelimart.com":
            self.set_header("Content-Type", "text/css")
            with open("/root/maxima/kelimart/i.css", "r") as kelimart_home_css:
                self.write(kelimart_home_css.read())
            kelimart_home_css.close()

class KelimartCookiesHand(tornado.web.RequestHandler):
    def get(self):
        if self.request.host=="kelimart.com" or self.request.host=="www.kelimart.com":
            self.set_status(200)
            self.set_header("Content-Type", "text/html")
            self.set_header("Access-Control-Allow-Origin", "*")
            self.set_header("Access-Control-Allow-Headers", "*")
            self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
            self.set_header("Access-Control-Max-Age", 1000)
            self.set_header("Access-Control-Allow-Headers", "*")
            with open("/root/maxima/kelimart/cookies/index.html", "r") as kelimart_cookies_html:
                self.write(kelimart_cookies_html.read())
            kelimart_cookies_html.close()
        else:
            self.set_status(404)

class MultiplierImageHand(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type", "image/png")
        with open("/root/maxima/images/multiplier_image.png", "rb") as maxima_img_multiplier:
            self.write(maxima_img_multiplier.read())
        maxima_img_multiplier.close()

class Favicon32Hand(tornado.web.RequestHandler):
    def get(self):
        if self.request.host=="kelimart.com" or self.request.host=="www.kelimart.com":
            self.set_header("Content-Type", "image/png")
            with open("/root/maxima/kelimart/images/Faroe_Logo_32.png", "rb") as kelimart_favicon_32:
                self.write(kelimart_favicon_32.read())
            kelimart_favicon_32.close()

class Favicon64Hand(tornado.web.RequestHandler):
    def get(self):
        if self.request.host=="kelimart.com" or self.request.host=="www.kelimart.com":
            self.set_header("Content-Type", "image/png")
            with open("/root/maxima/kelimart/images/Faroe_Logo_64.png", "rb") as kelimart_favicon_64:
                self.write(kelimart_favicon_64.read())
            kelimart_favicon_64.close()

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", HomeHTMLHand),
        (r"/pull/i.css", HomeCSSHand),
        (r"/images/multiplier_image.png", MultiplierImageHand),
        (r"/images/favicon32.png", Favicon32Hand),
        (r"/cookies/", KelimartCookiesHand),
        (r"/images/favicon64.png", Favicon64Hand)
    ])
  
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
