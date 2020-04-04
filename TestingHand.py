from udf import *

class handler(tornado.web.RequestHandler):
    def get(self):
        VerifyIndex = ServePage(self,"/sign_up/verified.html")
        VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>","<div id=\"rg_block\" hg=\"uc\"><h1>Welcome to Franzar!</h1></div>")
        self.write(VerifyIndex)
    
    def post(self):
        SetCookie(self)
