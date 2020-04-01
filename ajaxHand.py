from udf import *

# Don't forget to eventually close the MySQL connection

class AddToCartAjax(tornado.web.RequestHandler):
    def post(self):
        ATCRequest = urllib.parse.unquote(self.request.body.decode('utf-8'))
        if self.get_secure_cookie("Fu"):
            UserInfoFu = int(self.get_secure_cookie("Fu"))
            if ATCRequest.find("id=") >= 0 and ATCRequest.find("&qty=") >= 0:
                ATCRequestID = int(ATCRequest[(ATCRequest.index("id=")+3):ATCRequest.index("&qty=")])
                ATCRequestQty = int(ATCRequest[(ATCRequest.index("&qty=")+5):len(ATCRequest)])
                UserCartQuery = "INSERT INTO cart (uid,pid,qty) VALUES({0:d},{1:d},{2:d})".format(UserInfoFu,ATCRequestID,ATCRequestQty)
                mycursor.execute(UserCartQuery)
                db.commit()
                self.write("A")
            else:
                self.write("E_A")
        else:
            self.write("E_B")
