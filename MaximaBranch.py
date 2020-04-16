import os,tornado.web,tornado.ioloop
import HomeHand,AboutHand,ContactHand
import SignInHand,ForgotPWHand,ResetPWHand
import SignUpHand,VerifyHand
import AccountHand,ChangeLocalesAjax
import ProductHand,CartHand
import AddToCartAjax,RefreshCartAjax
import TestingHand
import InfoHand

class handler(tornado.web.RequestHandler):
    def get(self):
        print(self.request.host)
        if self.request.path == "/":
            HomeHand.handler(self)
