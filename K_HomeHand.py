from udf import *

def handler(self):
    CreateCookie(self,"FF","HelloWorld",100000000)
    # Generate Products List
    HomeProductList = ""
    mycursor.execute("SELECT id,ttl,price_"+UserCurrency.lower()+",discount,colour,colour_name FROM products WHERE disp=1 GROUP BY left(id,7)")
    QueryProductsDict = mycursor.fetchall()
    for i in range(0,len(QueryProductsDict)):
        QueryProductsPrice = float(QueryProductsDict[i][2])
        QueryProductsDiscountIntPre = int(QueryProductsDict[i][3])
        QueryProductsDiscountInt = (float(QueryProductsDict[i][2]) * ((100 - int(QueryProductsDiscountIntPre)) / 100))
        if UserCurrencySymbol in SpecifyCurrencyList:
            if QueryProductsDiscountIntPre > 0:
                QueryProductsPriceSet = "<h1><strike>{1:s}{2:,.2f}</strike></h1><h2>{1}{3:,.2f} ({0:s})</h2>".format(UserCurrency,UserCurrencySymbol,QueryProductsPrice,QueryProductsDiscountInt)
            else:
                QueryProductsPriceSet = "<h1>{1:s}{2:,.2f} ({0:s})</h1>".format(UserCurrency,UserCurrencySymbol,QueryProductsPrice)
        else:
            if QueryProductsDiscountIntPre > 0:
                QueryProductsPriceSet = "<h1><strike>{0:s}{1:,.2f}</strike></h1><h2>{0:s}{2:,.2f}</h2>".format(UserCurrencySymbol,QueryProductsPrice,QueryProductsDiscountInt)
            else:
                QueryProductsPriceSet = "<h1>{0:s}{1:,.2f}</h1>".format(UserCurrencySymbol,QueryProductsPrice)
        QueryProductsID = str(QueryProductsDict[i][0])
        QueryProductsDefaultColour = str(QueryProductsDict[i][4])
        QueryProductsDefaultColourName = str(QueryProductsDict[i][5]).title()
        QueryProductColoursDict = FindProductColours(QueryProductsID)
        ReturnProductTitle = str(QueryProductsDict[i][1])
        ReturnProductColoursDict = ""
        for Ci in range(0,len(QueryProductColoursDict["ID"])):
            if QueryProductColoursDict["Hex"][Ci] != QueryProductsDefaultColour:
                ReturnProductColoursDict += "<abbr style=\"background:#"+QueryProductColoursDict["Hex"][Ci]+";\" title=\""+QueryProductColoursDict["Name"][Ci]+"\" s=\"n\"></abbr>"
        HomeProductList += "<a style=\"background-image:url(/static/product/"+QueryProductsID+"/0.jpg);\" href=\"/product/"+QueryProductsID+"/\" title=\""+ReturnProductTitle+"\"><div class=\"BPX\"><span><abbr style=\"background:#"+QueryProductsDefaultColour+";\" title=\""+QueryProductsDefaultColourName+"\" s=\"y\"></abbr>"+ReturnProductColoursDict+"</span><h6>"+ReturnProductTitle+"</h6>"+QueryProductsPriceSet+"</div></a>\n"

    # Open
    HomeIndex = ServePage(self,"/index.html",False)
    HomeIndex = HomeIndex.replace("<% Products %>", HomeProductList)
    self.write(HomeIndex)

def post(self):
    AcceptCookies(self)
