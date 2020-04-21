from udf import *

class handler(tornado.web.RequestHandler):
    def get(self):
        # Open
        HomeIndex = ServePage(self,"/about/index.html",False)
        self.write(HomeIndex)
        
    def post(self):
        SetCookie(self)
