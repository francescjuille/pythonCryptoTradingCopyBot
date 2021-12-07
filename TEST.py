from Binance.config import clientBinance as BINANCE
from Binance.Account import Account
from Binance.Orders import Orders
from Binance.CryptoInfo import CryptoInfo
from Algoritms.AlgoritmPercentSell import AlgoritmPercentSell
from Bots.BotBasicLogic import BotBasicLogic
account=Account()
cryptoInfo=CryptoInfo()
order= Orders()
print("Program Init")
# print("account: "+str(account.getTotalMoneyInWallet("BUSD")))
algoritmPercentSell = AlgoritmPercentSell("DOGE","USDT",0.01)
print(algoritmPercentSell.sell())
# bot=BotBasicLogic(AlgoritmPercentSell("BUSDUSDT","BUSD","USDT",0.01))
# bot.startBot()

# print("checkIfSellTime: "+str(algoritm10PercentSell.checkIfSellTime()))
# print("checkIfBuyTime: "+str(algoritm10PercentSell.checkIfBuyTime()))