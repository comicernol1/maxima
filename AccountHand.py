from udf import *

class handler(tornado.web.RequestHandler):
    def get(self):
        if CheckLogin(self):
            UserInfoFu = self.get_cookie("Fu")
            # Pull Account Orders
            AccountOrdersQuery = "SELECT oid,pid,fprice,stat,arrival,dest from orders where uid='{0:d}' order by pdate desc".format(int(UserInfoFu))
            mycursor.execute(AccountOrdersQuery)
            AccountOrdersFetch = mycursor.fetchall()
            
            # Set OrderList
            AccountOrdersList = ""
            for OFi in range(0,len(AccountOrdersFetch)):
                AccountOrdersListStatus = ShippingCodesList[AccountOrdersFetch[OFi][3]]
                AccountOrdersList += "<tr>"
                AccountOrdersList += "<td><a href=\"/order/"+str(AccountOrdersFetch[OFi][0])+"/\">"+str(AccountOrdersFetch[OFi][0])+"</a></td>"
                AccountOrdersList += "<td><a href=\"/product/"+str(AccountOrdersFetch[OFi][1])+"/\">"+str(FindProduct(AccountOrdersFetch[OFi][1])["Name"])+"</a></td>"
                AccountOrdersList += "<td>$"+str(AccountOrdersFetch[OFi][2])+"</td>"
                AccountOrdersList += "<td>"+str(AccountOrdersListStatus)+"</td>"
                AccountOrdersList += "<td>"+str(AccountOrdersFetch[OFi][4])+"</td>"
                AccountOrdersList += "<td>"+str(FindAddress(AccountOrdersFetch[OFi][5])["StAddA"])+"</td>"
                AccountOrdersList += "</tr>\n"
            
            # Pull Account Addresses
            AccountAddressesQuery = "SELECT adid,stadda,staddb,city,zip,prov,ntn from addresses where uid='{0:d}' order by name asc".format(int(UserInfoFu))
            mycursor.execute(AccountAddressesQuery)
            AccountAddressesFetch = mycursor.fetchall()
            
            # Set AddressOptions
            if AccountAddressesFetch:
                AccountAddressOptions = ""
                for AFi in range(0,len(AccountAddressesFetch)):
                    AccountAddressOptions += "<option value=\""+str(AccountAddressesFetch[AFi][0])+"\">"+str(AccountAddressesFetch[AFi][1])+", "+str(AccountAddressesFetch[AFi][3])+" "+str(AccountAddressesFetch[AFi][4])+"</option>\n"
            else:
                AccountAddressOptions = "<option value=\"na\"> - Please Connect an Address - </option>"
            
            # Open
            AccountIndex = ServePage(self,"/account/index.html")
            AccountIndex = AccountIndex.replace("<% AddressOptions %>",AccountAddressOptions)
            AccountIndex = AccountIndex.replace("<% OrderList %>",AccountOrdersList)
            self.write(AccountIndex)
        else:
            self.redirect("/sign_in/")
    
    def post(self):
        SetCookie(self)
