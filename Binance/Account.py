from Binance.config import clientBinance as BINANCE
from Binance.CryptoInfo import CryptoInfo

class Account:

    def __init__(self):
        pass

    def getTotalMoneyInWallet(self, simbol):
        return float(BINANCE.get_asset_balance(simbol)["free"])

    def getDepositHistory(self):
        return BINANCE.get_deposit_history() 