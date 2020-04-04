from udf import *

class handler(tornado.web.RequestHandler):
    def get(self):
        VerifyIndex = ServePage(self,"/sign_up/verified.html")
        VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>","<div id=\"rg_block\" hg=\"uc\"><h1>Welcome to Franzar!</h1><div id=\"suc_i\"></div><h3>As a sign of appreciation for making it this far, we've added a FREE tailor's ruler to your cart. You'll need this if you want to order custom tailored clothes from us. To see your cart, you can click the button below or the shopping cart icon in the top-right corner.</h3><a href=\"/cart/\"><button class=\"rgsb\" id=\"Vuc_L\">Open Cart</button></a></div>")
        self.write(VerifyIndex)
    
    def post(self):
        SetCookie(self)
