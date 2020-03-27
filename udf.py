import os,random,base64,fnmatch,tornado.web,urllib.parse,mysql.connector,smtplib
from cryptography.fernet import Fernet
Enc32a = Fernet(base64.b64encode(os.environ["Enc32a"].encode()))
Enc32b = Fernet(base64.b64encode(os.environ["Enc32b"].encode()))

db = mysql.connector.connect(
    host = "127.0.0.1",
    port = 3306,
    user = "maxima",
    password = str(os.environ["MYSQL_MAXIMA_PASSWD"]),
    database = "franzar"
)
mycursor = db.cursor()

def CheckLogin(self):
    if self.get_secure_cookie("Fu") and self.get_secure_cookie("Ft"):
        UserInfoFu = self.get_secure_cookie("Fu")
        UserInfoFt = self.get_secure_cookie("Ft")
        UserInfoLoginQuery = "SELECT * from compacc where userid='{0:d}' and token='{1:d}'".format(int(UserInfoFu),int(UserInfoFt))
        mycursor.execute(UserInfoLoginQuery)
        UserInfoLoginFetch = mycursor.fetchone()
        if UserInfoLoginFetch:
            return True
        else:
            return False
    else:
        return False

def ServePage(self,pageloc):
    # Define Basics
    HeaderLISignIn = "<a id=\"HMs\" href=\"/sign_in/\">Sign In</a>"
    HeaderLIAccountButton = "<a id=\"HMs\" href=\"/account/\">My Account<span></span></a><a id=\"HMc\" href=\"/cart/\" title=\"My Cart\"><span>0</span></a>"
    CookieNotifDiv = "<div id=\"Fackc\">By continuing to use this site, you agree to our <a href=\"/legal/cookie_policy/\">Cookie Policy</a>. <b onclick=\"ackc()\">Accept</b></div>"
    
    # Define Header Pre
    if pageloc=="/index.html":
        HeaderLIPre = "<div id=\"M_H_close\" onclick=\"M_menu_hide()\"></div><li><a href=\"/\"><b>Home</b></a></li><li><a href=\"/contact/\">Contact</a></li>"
    elif pageloc=="/contact/index.html" or pageloc=="/contact/sent.html":
        HeaderLIPre = "<div id=\"M_H_close\" onclick=\"M_menu_hide()\"></div><li><a href=\"/\">Home</a></li><li><a href=\"/contact/\"><b>Contact</b></a></li>"
    else:
        HeaderLIPre = "<div id=\"M_H_close\" onclick=\"M_menu_hide()\"></div><li><a href=\"/\">Home</a></li><li><a href=\"/contact/\">Contact</a></li>"
    
    # Open Templates
    with open("/root/maxima/templates/head.html") as HeadHTML_F:
        HeadHTML = HeadHTML_F.read()
    with open("/root/maxima/templates/footer.html") as FooterHTML_F:
        FooterHTML = FooterHTML_F.read()
    
    # Open Requested Page
    with open("/root/maxima/req"+str(pageloc)) as PageIndex_F:
        PageIndex = PageIndex_F.read()
    if CheckLogin(self):
        PageIndex = PageIndex.replace("<% HeaderLI %>",HeaderLIPre+HeaderLIAccountButton)
    else:
        PageIndex = PageIndex.replace("<% HeaderLI %>",HeaderLIPre+HeaderLISignIn)
    PageIndex = PageIndex.replace("<% Head %>",HeadHTML)
    if self.get_secure_cookie("Fa") == "true":
        FooterHTML = FooterHTML.replace("<% CookieNotif %>","")
    else:
        FooterHTML = FooterHTML.replace("<% CookieNotif %>",CookieNotifDiv)
    PageIndex = PageIndex.replace("<% Footer %>",FooterHTML)
    return PageIndex
    
def FindAddress(adid):
    try:
        FindAddressQuery = "SELECT stadda,staddb,city,zip,prov,ntn from addresses where adid='{0:d}'".format(int(adid))
        mycursor.execute(FindAddressQuery)
        FindAddressFetch = mycursor.fetchone()
        if FindAddressFetch:
            FindAddressStAddA = FindAddressFetch[0]
            FindAddressStAddB = FindAddressFetch[1]
            FindAddressCity = FindAddressFetch[2]
            FindAddressZip = FindAddressFetch[3]
            FindAddressProv = FindAddressFetch[4]
            FindAddressNtn = FindAddressFetch[5]
            FindAddressDict = {"StAddA":FindAddressStAddA,"StAddB":FindAddressStAddB,"City":FindAddressCity,"Zip":FindAddressZip,"Prov":FindAddressProv,"Ntn":FindAddressNtn}
            return FindAddressDict
        else:
            return {"StAddA":"","StAddB":"","City":"","Zip":"","Prov":"","Ntn":""}
    except:
        return {"StAddA":"","StAddB":"","City":"","Zip":"","Prov":"","Ntn":""}
