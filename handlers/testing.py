from udf import *

class TestingHand(tornado.web.RequestHandler):
    def get(self):
        self.set_cookie("Fu","0123456789")
    
    def post(self):
        SetCookie(self)
