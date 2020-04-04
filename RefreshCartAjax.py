class handler(tornado.web.RequestHandler):
    def get(self):
        NotFoundIndex = ServePage(self,"/status/404.html")
        self.write(NotFoundIndex)
        
    def post(self):
        RFCRequest = urllib.parse.unquote(self.request.body.decode('utf-8'))
        if self.get_cookie("Fu"):
            UserInfoFu = int(self.get_cookie("Fu"))
            RFCQuery = "DELETE FROM cart WHERE uid={0:d}".format(UserInfoFu)
            mycursor.execute(RFCQuery)
            RFCValList = []
            RFCRequestCnt = RFCRequest.count("&id")
            for i in range(0,RFCRequestCnt):
                RFCRequestID = int(RFCRequest[(RFCRequest.find("&id"+str(i)+"=")+4+len(str(i))):RFCRequest.find("&qty"+str(i)+"=")])
                if i<(RFCRequestCnt-1):
                    RFCRequestQty = int(RFCRequest[(RFCRequest.find("&qty"+str(i)+"=")+5+len(str(i))):RFCRequest.find("&id"+str(i+1)+"=")])
                else:
                    RFCRequestQty = int(RFCRequest[(RFCRequest.find("&qty"+str(i)+"=")+5+len(str(i))):])
                RFCValTuple = (UserInfoFu,RFCRequestID,RFCRequestQty)
                RFCValList.append(RFCValTuple)
            RFCQuery = "INSERT INTO cart (uid,pid,qty) VALUES(%s,%s,%s)"
            mycursor.executemany(RFCQuery,RFCValList)
            db.commit()
            self.write("A")
        else:
            self.write("E_B")
