from Binance.config import clientBinance as BINANCE
# EL que es compra va primer per exemple:  BTC_USDT -> comprar BTC en USDT
# el atribut price en BTC_USDT es el valor de BTC en dollars en que vols comprar BTC, per exemple quan BTC sigui igual a 51000 USDT, cantidad: cantidad de BTC
from Binance.Account import Account
from Binance.CryptoInfo import CryptoInfo

class Orders:

    cryptoInfo=CryptoInfo()

    def __init__(self):
        pass

    def createOrder(self,symbol,quantity,price=0,side="",marketPrice=False):
        #quantity=quantity*0.999
        simbolInfo=self.cryptoInfo.getSymbolInfo(symbol)
        minQty=-1
        for i in simbolInfo["filters"]:
            if(i["filterType"]=="LOT_SIZE"):
                minQty=i["minQty"]
        print("cantidad minima: "+minQty)        
        #minQty=float(minQty)
        minQty=str(minQty).split(".")
        print("split: "+str(minQty))

        if(int(minQty[1])==0):
            quantity=str(int(quantity))

        else:
            numberOf0=0
            for i in minQty[1]:
                if(i=="0"):
                    numberOf0+=1
                else:
                    break
            print("numberOf0: "+str(numberOf0))
            print("quantity: "+str(quantity))
            spl=str(quantity).split(".")
            newFloat=""
            c=0
            for i in spl[1]:
                if(c<=numberOf0):
                    newFloat+=i
                else:
                    break    
                c+=1

            quantity=spl[0]+"."+newFloat


        print("quantity: "+str(quantity))
        precision=simbolInfo["baseAssetPrecision"]
        price=round(price,precision)
        price=self.cryptoInfo.addDecimals(str(price),precision-self.cryptoInfo.getDecimalsLength(price))

        result=None
        if(marketPrice):
            result=BINANCE.create_order(
                symbol=symbol,
                side=side,
                type=BINANCE.ORDER_TYPE_MARKET, 
                quantity=str(quantity))
        else:
            result=BINANCE.create_order(
                symbol=symbol,
                side=side,
                type=BINANCE.ORDER_TYPE_LIMIT,
                timeInForce=BINANCE.TIME_IN_FORCE_GTC,
                quantity=str(quantity),
                price=str(price))
        return result

    def orderStatus(self,symbol,orderId):
        orderStatus = BINANCE.get_order(
            symbol=symbol,
            orderId=orderId)
        return orderStatus

    def getLastOrder(self,symbol):
        orders=BINANCE.get_all_orders(symbol=symbol, limit=1000)
        if(len(orders)>0):
            return orders[len(orders)-1]
        return None
     