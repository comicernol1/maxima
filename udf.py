import os,random,base64,fnmatch,tornado.web,urllib.parse,mysql.connector,smtplib

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
