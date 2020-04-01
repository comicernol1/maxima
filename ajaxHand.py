from udf import *

# Don't forget to eventually close the MySQL connection

class AddToCartAjax(tornado.web.RequestHandler):
    def post(self):
        AddToCartRequest = self.request.body.decode('utf-8')
        print(AddToCartRequest)
