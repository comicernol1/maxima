from udf import *

class handler(tornado.web.RequestHandler):
    def get(self):
        self.write(tornado.locale.get_supported_locales())
        # VerifyIndex = ServePage(self,"/sign_up/verified.html",False)
        # VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>","<div id=\"rg_block\" hg=\"ue\">This Email is already verified</div>")
        # self.write(VerifyIndex)
    
    def post(self):
        SetCookie(self)
