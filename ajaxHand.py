from udf import *

# Don't forget to eventually close the MySQL connection

class AddToCartAjax(tornado.web.RequestHandler):
    def post(self):
        ATCRequest = urllib.parse.unquote(self.request.body.decode('utf-8'))
        if self.get_secure_cookie("Fu"):
            UserInfoFu = self.get_secure_cookie("Fu").decode('utf-8')
            if ATCRequest.find("id=") >= 0 and ATCRequest.find("&qty=") >= 0:
                ATCRequestID = ATCRequest[(ATCRequest.index("id=")+3):ATCRequest.index("&qty=")]
                ATCRequestQty = ATCRequest[(ATCRequest.index("&qty=")+5):len(ATCRequest)]
                print(UserInfoFu)
                return "Success"
            else:
                print("Error A")
        else:
            print("Error B")
