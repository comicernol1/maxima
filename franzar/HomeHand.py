from udf import *

class handler(tornado.web.RequestHandler):
    def get(self):
        # Open
        HomeIndex = ServePage(self,"/index.html",False)
        self.write(HomeIndex)

    def post(self):
        AcceptCookies(self)
