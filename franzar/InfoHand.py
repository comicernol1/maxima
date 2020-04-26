from udf import *

class TermsConditions(tornado.web.RequestHandler):
    def get(self):
        # Open
        TermsConditionsIndex = ServePage(self,"/legal/terms.html",False)
        self.write(TermsConditionsIndex)
    
    def post(self):
        SetCookie(self)

class Counterfeit(tornado.web.RequestHandler):
    def get(self):
        # Open
        CounterfeitIndex = ServePage(self,"/legal/counterfeit.html",False)
        self.write(CounterfeitIndex)
    
    def post(self):
        SetCookie(self)

class Returns(tornado.web.RequestHandler):
    def get(self):
        # Open
        ReturnsIndex = ServePage(self,"/legal/returns.html",False)
        self.write(ReturnsIndex)
    
    def post(self):
        SetCookie(self)

class NotFound(tornado.web.RequestHandler):
    def get(self):
        # Open
        NotFoundIndex = ServePage(self,"/status/404.html",False)
        self.write(NotFoundIndex)
    
    def post(self):
        SetCookie(self)
