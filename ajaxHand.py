from udf import *

# Don't forget to eventually close the MySQL connection

class AddToCartAjax(tornado.web.RequestHandler):
    def post(self):
        ATCRequest = urllib.parse.unquote(self.request.body.decode('utf-8'))
        if self.get_secure_cookie("Fu"):
            UserInfoFu = self.get_secure_cookie("Fu")
            if ATCRequest.find("id=") and ATCRequest.find("&qty="):
                ATCRequestID = ContactRequestBody[(ContactRequestBody.index("id=")+3):ContactRequestBody.index("&qty=")]
                ATCRequestQty = ContactRequestBody[(ContactRequestBody.index("&qty=")+5):len(ContactRequestBody)]
                print(UserInfoFu)
            else:
                print("Error A")
        else:
            print("Error B")
