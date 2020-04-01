from udf import *

# Don't forget to eventually close the MySQL connection

class AddToCartAjax(tornado.web.RequestHandler):
    def post(self):
        ATCRequest = urllib.parse.unquote(self.request.body.decode('utf-8'))
        if self.get_secure_cookie("Fu"):
            UserInfoFu = self.get_secure_cookie("Fu")
            if ATCRequest.find("id=") and ATCRequest.find("&qty="):
                ATCRequestID = ATCRequest[(ATCRequest.index("id=")+3):ATCRequest.index("&qty=")]
                ATCRequestQty = ATCRequest[(ATCRequest.index("&qty=")+5):len(ATCRequest)]
                print(UserInfoFu)
            else:
                print("Error A - "+ATCRequest)
        else:
            print("Error B")
