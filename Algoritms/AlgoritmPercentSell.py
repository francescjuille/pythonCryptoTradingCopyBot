import sys
sys.path.append(".")

from Binance.config import clientBinance as BINANCE
from Binance.Account import Account
from Binance.Orders import Orders
from Binance.CryptoInfo import CryptoInfo

""" 
If the price of some symbol, for example (BNBBUSD) is 10% UP in less than 10 hours, execute sell action and only buy again when the value is 10% OFF
"""

class AlgoritmPercentSell:
    
    symbol=""
    firstSymbol=""
    secondSymbol=""
    persentSellBuy=0.01
    account=Account()
    orders=Orders()
    cryptoInfo=CryptoInfo()
    
    def __init__(self,firstSymbol,secondSymbol,persentSellBuy):
        self.symbol=firstSymbol+secondSymbol
        print("self.symbol: "+str(self.symbol))
        self.firstSymbol=firstSymbol
        self.secondSymbol=secondSymbol
        self.persentSellBuy=persentSellBuy

    def checkIfSellTime(self):
        lastOrder=self.orders.getLastOrder(self.symbol)
        actualPrice=self.cryptoInfo.getSimbolPrice(self.symbol)
        #print("float(lastOrder[price]): "+str(float(lastOrder["price"])))
        #print("float(actualPrice) - (float(lastOrder[price])*0.03: "+str(float(actualPrice) - (float(lastOrder["price"])*0.03)))
        if(lastOrder["status"]=='FILLED' and lastOrder["side"]=='BUY' and float(lastOrder["price"]) < float(actualPrice) - (float(lastOrder["price"])*self.persentSellBuy)):
            return True

        """
        history=self.cryptoInfo.getHistoricalCryptoPrice(self.symbol, "8")
        lenList=len(history)-1
        actualPrice = history[lenList][2]
        for i in range(history):
            value = history[lenList-i][2]
            if(actualPrice > value+(value*0.1)):
                return True
        """        
        return False

    def checkIfBuyTime(self):
        actualPrice=self.cryptoInfo.getSimbolPrice(self.symbol)
        lastOrder=self.orders.getLastOrder(self.symbol)
        if(lastOrder["status"]=='FILLED' and lastOrder["side"]=='SELL' and float(lastOrder["price"]) > float(actualPrice) + (float(lastOrder["price"])*self.persentSellBuy)):
            return True
        return False    

    def buy(self):
        price=self.cryptoInfo.getSimbolPrice(self.symbol)
        quantity=(self.account.getTotalMoneyInWallet(self.secondSymbol) * (1/price))
        print("BUY")
        print("price: "+str(price))
        print("quantiti: "+str(quantity))
        print("__________")
        return self.orders.createOrder(self.symbol,quantity,price,BINANCE.SIDE_BUY,marketPrice=True)

    def sell(self):
        price=self.cryptoInfo.getSimbolPrice(self.symbol)
        quantity=self.account.getTotalMoneyInWallet(self.firstSymbol)
        print("SELL")
        print("price: "+str(price))
        print("quantiti: "+str(quantity))
        print("___________")
        return self.orders.createOrder(self.symbol,quantity,price,BINANCE.SIDE_SELL,marketPrice=True)
    