from Binance.config import clientBinance as BINANCE

class CryptoInfo:

    def __init__(self):
        pass

    def getSimbolPrice(self, symbol):
        allPrices=BINANCE.get_all_tickers()
        for i in allPrices:
            if(i["symbol"]==symbol):
                return round(float(i["price"]),6)
        return None

    def getHistoricalCryptoPrice(self, symbol, hoursAgo):
        historial=BINANCE.get_historical_klines_generator(symbol, BINANCE.KLINE_INTERVAL_5MINUTE, hoursAgo+" hours ago UTC")
        for kline in historial:
            print(kline)
        return historial

    def getSymbolInfo(self,symbol):
        a=BINANCE.get_symbol_info(symbol)
        print(a)
        try:
            return a
        except:
            return None

    def getDecimalsLength(self,number):  
        a=str(number).split(".")   
        return (len(a[1]))

    def addDecimals(self,number,numDecimalsToAdd):
        for i in range(numDecimalsToAdd):
            number+="0"
        return number
