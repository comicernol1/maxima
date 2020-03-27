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
