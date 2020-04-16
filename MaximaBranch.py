import os,tornado.web,tornado.ioloop
import HomeHand,AboutHand,ContactHand
import SignInHand,ForgotPWHand,ResetPWHand
import SignUpHand,VerifyHand
import AccountHand,ChangeLocalesAjax
import ProductHand,CartHand
import AddToCartAjax,RefreshCartAjax
import TestingHand
import InfoHand

print(tornado.web.RequestHandler.path_args)
