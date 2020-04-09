from udf import *

class handler(tornado.web.RequestHandler):
    def get(self):
        NotFoundIndex = ServePage(self,"/status/404.html",False)
        self.write(NotFoundIndex)
        
    def post(self):
        LOCRequest = urllib.parse.unquote(self.request.body.decode('utf-8'))
        if self.get_cookie("Fa"):
            if self.get_cookie("Fa") == "true":
                if LOCRequest.find("nt=") >= 0 and LOCRequest.find("&lg=") >= 0:
                    LOCRequestNation = LOCRequest[(LOCRequest.index("nt=")+3):LOCRequest.index("&lg=")]
                    LOCRequestLanguage = LOCRequest[(LOCRequest.index("&lg=")+4):len(LOCRequest)]
                    self.set_cookie("Fn",LOCRequestNation)
                    self.set_cookie("FL",LOCRequestLanguage)
                    self.write("A")
                else:
                    self.write("E_A")
            else:
                self.write("E_B")
        else:
            self.write("E_C")
