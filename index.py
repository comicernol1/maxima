import os
import tornado.web
import tornado.ioloop
from tornado.routing import HostMatches
from settings import settings

import kelimart.AboutHand
import kelimart.AccountHand
import kelimart.AddToCartAjax
import kelimart.CartHand
import kelimart.ChangeLocalesAjax
import kelimart.ContactHand
import kelimart.ForgotPWHand
import kelimart.HomeHand
import kelimart.InfoHand
import kelimart.ProductHand
import kelimart.RefreshCartAjax
import kelimart.ResetPWHand
import kelimart.SignInHand
import kelimart.SignUpHand
import kelimart.TestingHand
import kelimart.VerifyHand

import franzar.HomeHand

class RedirectRemoveWWW(tornado.web.RequestHandler):
    def prepare(self):
        self.redirect("https://google.com/"+self.request.uri)
        # self.write(self.request.host)

if __name__ == "__main__":
    app = tornado.web.Application([
        (HostMatches("kelimart.com"), [
            (r"/about_us/", kelimart.AboutHand.handler),
            (r"/account/", kelimart.AccountHand.handler),
            (r"/add_to_cart/", kelimart.AddToCartAjax.handler),
            (r"/cart/", kelimart.CartHand.handler),
            (r"/account/locales/", kelimart.ChangeLocalesAjax.handler),
            (r"/contact/", kelimart.ContactHand.handler),
            (r"/sign_in/forgot_password/", kelimart.ForgotPWHand.handler),
            (r"/", kelimart.HomeHand.handler),
            (r"/legal/terms_and_conditions/", kelimart.InfoHand.TermsConditions),
            (r"/report_a_counterfeit/", kelimart.InfoHand.Counterfeit),
            (r"/product/.*", kelimart.ProductHand.handler),
            (r"/refresh_cart/", kelimart.RefreshCartAjax.handler),
            (r"/sign_in/reset_password/", kelimart.ResetPWHand.handler),
            (r"/sign_in/", kelimart.SignInHand.handler),
            (r"/sign_up/", kelimart.SignUpHand.handler),
            (r"/test/", kelimart.TestingHand.handler),
            (r"/verify/", kelimart.VerifyHand.handler),
            (r"/.*", kelimart.InfoHand.NotFound)
        ]),
        (HostMatches("www.kelimart.com"), [
            (r"/", RedirectRemoveWWW)
        ]),
        
        (HostMatches("franzar.com"), [
            (r"/", franzar.HomeHand.handler)
        ])
    ], **settings)

    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
