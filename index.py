import os,tornado.web,tornado.ioloop

with open("/root/maxima/kelimart/req/index.html", "r") as home_icnt_f:
    home_icnt = home_icnt_f.read()
class homeHTMLHandler(tornado.web.RequestHandler):
    def get(self):
        if self.request.host=="kelimart.com":
            self.set_header('Content-Type', 'text/html')
            self.write(home_icnt)
        else:
            self.write(self.request.host)
        
with open("/root/maxima/kelimart/req/i.css", "r") as home_scnt_f:
    home_scnt = home_scnt_f.read()
class homeCSSHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'text/css')
        self.write(home_scnt)

with open("/root/maxima/images/multiplier_image.png", "rb") as mult_pcnt_f:
    mult_pcnt = mult_pcnt_f.read()

class ImageHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'image/png')
        self.write(mult_pcnt)
        
with open("/root/maxima/kelimart/images/Faroe_Logo_64.png", "rb") as fav64_pcnt_f:
    fav64_pcnt = fav64_pcnt_f.read()
class Favicon64Handler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'image/png')
        self.write(fav64_pcnt)
    
if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", homeHTMLHandler),
        (r"/pull/i.css", homeCSSHandler),
        (r"/images/multiplier_image.png", ImageHandler),
        (r"/images/Faroe_Logo_64.png", Favicon64Handler)
    ])
  
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
