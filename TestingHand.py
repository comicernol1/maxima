from udf import *

class handler(tornado.web.RequestHandler):
    def get(self):
        VerifyIndex = ServePage(self,"/sign_up/verified.html")
        VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>","")
        self.write(VerifyIndex)
    
    def post(self):
        SetCookie(self)
