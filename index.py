import os,tornado.web,tornado.ioloop

with open("/root/maxima/kelimart/index.html", "r") as kelimart_home_html_f:
    kelimart_home_html = kelimart_home_html_f.read()
class homeHTMLHandler(tornado.web.RequestHandler):
    def get(self):
        if self.request.host=="kelimart.com":
            self.set_header('Content-Type', 'text/html')
            self.write(kelimart_home_html)
        
with open("/root/maxima/kelimart/i.css", "r") as kelimart_home_css_f:
    kelimart_home_css = kelimart_home_css_f.read()
class homeCSSHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'text/css')
        self.write(kelimart_home_css)

with open("/root/maxima/images/multiplier_image.png", "rb") as maxima_img_multiplier_f:
    maxima_img_multiplier = maxima_img_multiplier_f.read()
class MultiplierImageHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'image/png')
        self.write(maxima_img_multiplier)
        
with open("/root/maxima/kelimart/images/Faroe_Logo_64.png", "rb") as kelimart_favicon_64_f:
    kelimart_favicon_64 = kelimart_favicon_64_f.read()
class Favicon64Handler(tornado.web.RequestHandler):
    def get(self):
        if self.request.host=="kelimart.com":
            self.set_header('Content-Type', 'image/png')
            self.write(kelimart_favicon_64)
    
if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", homeHTMLHandler),
        (r"/pull/i.css", homeCSSHandler),
        (r"/images/multiplier_image.png", MultiplierImageHandler),
        (r"/images/Faroe_Logo_64.png", Favicon64Handler)
    ])
  
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
