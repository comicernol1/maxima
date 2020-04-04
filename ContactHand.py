from udf import *

class handler(tornado.web.RequestHandler):
    def get(self):
        # Open
        ContactIndex = ServePage(self,"/contact/index.html",False)
        ContactIndex = ContactIndex.replace("<% ShowError %>","none")
        ContactIndex = ContactIndex.replace("<% ErrorMsg %>","")
        self.write(ContactIndex)
        
    def post(self):
        # Open
        ContactIndex = ServePage(self,"/contact/index.html",False)
        ContactSentIndex = ServePage(self,"/contact/sent.html",False)
        
        # Test
        ContactRequestBody = urllib.parse.unquote(self.request.body.decode('utf-8').replace("+"," "))
        if ContactRequestBody.find("CFn=") >= 0 and ContactRequestBody.find("CFe=") >= 0 and ContactRequestBody.find("CFo=") >= 0 and ContactRequestBody.find("CFt=") >= 0:
            ContactRequestCFn = ContactRequestBody[(ContactRequestBody.index("CFn=")+4):ContactRequestBody.index("&CFe=")]
            ContactRequestCFe = ContactRequestBody[(ContactRequestBody.index("CFe=")+4):ContactRequestBody.index("&CFo=")]
            ContactRequestCFo = ContactRequestBody[(ContactRequestBody.index("CFo=")+4):ContactRequestBody.index("&CFt=")]
            ContactRequestCFt = ContactRequestBody[(ContactRequestBody.index("CFt=")+4):len(ContactRequestBody)]
            if ContactRequestCFn != "" and ValidEmail(ContactRequestCFe) and ContactRequestCFt != "":
                with open("/root/maxima/templates/contact/ticket.html") as ContactSMPTTemplate_T_F:
                    ContactSMTPTemplate_T = ContactSMPTTemplate_T_F.read()
                with open("/root/maxima/templates/contact/confirm.html") as ContactSMPTTemplate_U_F:
                    ContactSMTPTemplate_U = ContactSMPTTemplate_U_F.read()
                
                # Send Ticket Email
                ContactSMTPTemplate_T = ContactSMTPTemplate_T.replace("<% FullName %>",str(ContactRequestCFn))
                ContactSMTPTemplate_T = ContactSMTPTemplate_T.replace("<% Email %>",str(ContactRequestCFe))
                ContactSMTPTemplate_T = ContactSMTPTemplate_T.replace("<% OrderID %>",str(ContactRequestCFo))
                ContactSMTPTemplate_T = ContactSMTPTemplate_T.replace("<% Message %>",str(ContactRequestCFt))
                ContactSMTPTicketID = str(random.randint(10000,99999))
                ContactSMTPHeaders_T = "\r\n".join(["from: comicernol@gmail.com","subject: Ticket #"+ContactSMTPTicketID,"to:reedsienkiewicz@gmail.com","mime-version: 1.0","content-type: text/html"])
                ContactSMTPContent_T = ContactSMTPHeaders_T+"\r\n\r\n"+ContactSMTPTemplate_T
                ContactMail_T = smtplib.SMTP('smtp.gmail.com',587)
                ContactMail_T.ehlo()
                ContactMail_T.starttls()
                ContactMail_T.login('comicernol@gmail.com',str(os.environ["Comicernol_Gmail_Passwd"]))
                ContactMail_T.sendmail('comicernol@gmail.com','reedsienkiewicz@gmail.com',ContactSMTPContent_T)
                ContactMail_T.close()
                
                # Send User Confirmation Email
                ContactSMTPTemplate_U = ContactSMTPTemplate_U.replace("<% FullName %>",str(ContactRequestCFn))
                ContactSMTPTemplate_U = ContactSMTPTemplate_U.replace("<% Email %>",str(ContactRequestCFe))
                ContactSMTPTemplate_U = ContactSMTPTemplate_U.replace("<% OrderID %>",str(ContactRequestCFo))
                ContactSMTPTemplate_U = ContactSMTPTemplate_U.replace("<% Message %>",str(ContactRequestCFt))
                ContactSMTPHeaders_U = "\r\n".join(["from: comicernol@gmail.com","subject: Confirmation of Ticket #"+ContactSMTPTicketID,"to:"+str(ContactRequestCFe),"mime-version: 1.0","content-type: text/html"])
                ContactSMTPContent_U = ContactSMTPHeaders_U+"\r\n\r\n"+ContactSMTPTemplate_U
                ContactMail_U = smtplib.SMTP('smtp.gmail.com',587)
                ContactMail_U.ehlo()
                ContactMail_U.starttls()
                ContactMail_U.login('comicernol@gmail.com',str(os.environ["Comicernol_Gmail_Passwd"]))
                ContactMail_U.sendmail('comicernol@gmail.com',str(ContactRequestCFe),ContactSMTPContent_U)
                ContactMail_U.close()
                self.write(ContactSentIndex)
            else:
                if ContactRequestCFn=="":
                    ContactIndex = ContactIndex.replace("<% ErrorMsg %>","Please enter your name")
                elif not ValidEmail(ContactRequestCFe):
                    ContactIndex = ContactIndex.replace("<% ErrorMsg %>","Please enter a valid Email")
                elif ContactRequestCFt=="":
                    ContactIndex = ContactIndex.replace("<% ErrorMsg %>","Please enter your message")
                else:
                    ContactIndex = ContactIndex.replace("<% ErrorMsg %>","(C1) Something went wrong")
                ContactIndex = ContactIndex.replace("<% ShowError %>","block")
                self.write(ContactIndex)
        else:
            if SetCookie(self):
                pass
            else:
                ContactIndex = ContactIndex.replace("<% ErrorMsg %>","(C2) Something went wrong")
                ContactIndex = ContactIndex.replace("<% ShowError %>","block")
                self.write(ContactIndex)
