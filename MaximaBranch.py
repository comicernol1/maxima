import os,tornado.web,tornado.ioloop
import K_HomeHand
import F_HomeHand

class handler(tornado.web.RequestHandler):
    def get(self):
        if self.request.host == "kelimart.com" or self.request.host == "www.kelimart.com":
            if self.request.path == "/":
                K_HomeHand.handler(self)
        elif self.request.host == "franzar.com" or self.request.host == "www.franzar.com":
            if self.request.path == "/":
                F_HomeHand.handler(self)
        else:
            pass
