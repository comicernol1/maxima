from udf import *

class TermsConditions(tornado.web.RequestHandler):
    def get(self):
        # Open
        TermsConditionsIndex = ServePage(self,"/legal/terms.html")
        self.write(TermsConditionsIndex)
    
    def post(self):
        SetCookie(self)

class Counterfeit(tornado.web.RequestHandler):
    def get(self):
        # Open
        CounterfeitIndex = ServePage(self,"/legal/counterfeit.html")
        self.write(CounterfeitIndex)
    
    def post(self):
        SetCookie(self)

class NotFound(tornado.web.RequestHandler):
    def get(self):
        # Open
        NotFoundIndex = ServePage(self,"/status/404.html")
        self.write(NotFoundIndex)
    
    def post(self):
        SetCookie(self)
