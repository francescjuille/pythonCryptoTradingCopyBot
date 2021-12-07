import sys
sys.path.append(".")
import time
from datetime import datetime
import threading
from Binance.config import clientBinance as BINANCE
from Binance.config import reconnectToBinance

"""
Simple bot that execute the program algoritms each time without stop
"""

class BotBasicLogic:

    algoritm=None
    def __init__(self, algoritm):
        self.algoritm=algoritm

    def startBot(self):
        print("BOT STARTED")
        while(True):
            time.sleep(80)
            try:
                timeSell=self.algoritm.checkIfSellTime()
                timeBuy=self.algoritm.checkIfBuyTime()
                print("step - "+self.getCurrentTime())
                if timeSell and timeBuy:
                    print("**BREAK**")
                    break

                if timeSell:
                    print("\nSELL TIME")
                    self.algoritm.sell()
                    print("\n")

                if timeBuy:
                    print("\nBUY TIME")
                    self.algoritm.buy()
                    print("\n")
            except Exception as e:
                print("___________________________")
                print("ERROR EXCEPTION: "+str(e))
                print("->")
                reconnectToBinance()
                print("reconnected to Binance")
                print("___________________________")

                

    def startBotAsThread(self):
        x = threading.Thread(target=self.startBot)
        x.start()

    def getCurrentTime(self):
        now = datetime.now()
        current_time = now.strftime("%D - %H:%M:%S")
        return str(current_time)    