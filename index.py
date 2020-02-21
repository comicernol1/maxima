import os,tornado.web,tornado.ioloop

class HomeHTMLHand(tornado.web.RequestHandler):
    def get(self):
        if self.request.host=="kelimart.com" or self.request.host=="www.kelimart.com":
            self.set_header('Content-Type', 'text/html')
            with open("/root/maxima/kelimart/index.html", "r") as kelimart_home_html:
                self.write(kelimart_home_html.read())
            kelimart_home_html.close()

class HomeCSSHand(tornado.web.RequestHandler):
    def get(self):
        if self.request.host=="kelimart.com" or self.request.host=="www.kelimart.com":
            self.set_header('Content-Type', 'text/css')
            with open("/root/maxima/kelimart/i.css", "r") as kelimart_home_css:
                self.write(kelimart_home_css.read())
            kelimart_home_css.close()

class KelimartCookiesHand(tornado.web.RequestHandler):
    def get(self):
        if self.request.host=="kelimart.com" or self.request.host=="www.kelimart.com":
            self.set_header('Content-Type', 'text/html')
            with open("/root/maxima/kelimart/cookies/index.html", "r") as kelimart_cookies_html:
                self.write(kelimart_cookies_html.read())
            kelimart_cookies_html.close()

class MultiplierImageHand(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'image/png')
        with open("/root/maxima/images/multiplier_image.png", "rb") as maxima_img_multiplier:
            self.write(maxima_img_multiplier.read())
        maxima_img_multiplier.close()

class Favicon32Hand(tornado.web.RequestHandler):
    def get(self):
        if self.request.host=="kelimart.com" or self.request.host=="www.kelimart.com":
            self.set_header('Content-Type', 'image/png')
            with open("/root/maxima/kelimart/images/Faroe_Logo_32.png", "rb") as kelimart_favicon_32:
                self.write(kelimart_favicon_32.read())
            kelimart_favicon_32.close()

class Favicon64Hand(tornado.web.RequestHandler):
    def get(self):
        if self.request.host=="kelimart.com" or self.request.host=="www.kelimart.com":
            self.set_header('Content-Type', 'image/png')
            with open("/root/maxima/kelimart/images/Faroe_Logo_64.png", "rb") as kelimart_favicon_64:
                self.write(kelimart_favicon_64.read())
            kelimart_favicon_64.close()

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", HomeHTMLHand),
        (r"/pull/i.css", HomeCSSHand),
        (r"/images/multiplier_image.png", MultiplierImageHand),
        (r"/images/favicon32.png", Favicon32Hand),
        (r"/cookies/", KelimartCookiesHand),
        (r"/images/favicon64.png", Favicon64Hand)
    ])
  
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
