from udf import *

class handler(tornado.web.RequestHandler):
    def get(self):
        NotFoundIndex = ServePage(self,"/status/404.html",False)
        self.write(NotFoundIndex)
        
    def post(self):
        ATCRequest = urllib.parse.unquote(self.request.body.decode('utf-8'))
        if self.get_cookie("Fu"):
            UserInfoFu = int(self.get_cookie("Fu"))
            if ATCRequest.find("id=") >= 0 and ATCRequest.find("&qty=") >= 0:
                ATCRequestID = int(ATCRequest[(ATCRequest.index("id=")+3):ATCRequest.index("&qty=")])
                ATCRequestQty = int(ATCRequest[(ATCRequest.index("&qty=")+5):len(ATCRequest)])
                ATCCntQuery = "SELECT pid,qty FROM cart WHERE uid={0:d} AND pid={1:d}".format(UserInfoFu,ATCRequestID)
                mycursor.execute(ATCCntQuery)
                ATCCntFetch = mycursor.fetchone()
                if ATCCntFetch:
                    CartItemCurrentQty = int(ATCCntFetch[1])
                    if CartItemCurrentQty >= 10:
                        self.write("E_F")
                    else:
                        CartItemNewQty = (CartItemCurrentQty+ATCRequestQty)
                        ATCQuery = "UPDATE cart SET qty={0:d} WHERE uid={1:d} AND pid={2:d} LIMIT 1".format(CartItemNewQty,UserInfoFu,ATCRequestID)
                        mycursor.execute(ATCQuery)
                        db.commit()
                        self.write("A")
                else:
                    ATCQuery = "INSERT INTO cart (uid,pid,qty) VALUES({0:d},{1:d},{2:d})".format(UserInfoFu,ATCRequestID,ATCRequestQty)
                    mycursor.execute(ATCQuery)
                    db.commit()
                    self.write("A")
            else:
                self.write("E_A")
        else:
            self.write("E_B")
