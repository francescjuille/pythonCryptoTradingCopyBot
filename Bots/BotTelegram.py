import sys
sys.path.append(".")
import time, json
from datetime import datetime, timedelta
import threading
from Binance.config import clientBinance as BINANCE
from Binance.config import reconnectToBinance
from Apis.TelegramApi import TelegramApi

from Binance.Account import Account
from Binance.Orders import Orders
from Binance.CryptoInfo import CryptoInfo

"""
Simple bot that save signals from telegram
"""

class BotTelegram:

    telegram=None
    cryptoInfo=CryptoInfo()
    orders=Orders()
    account=Account()

    def __init__(self):
        self.telegram=TelegramApi()


    def startBot(self):
        print("TELEGRAM BOT STARTED")
        ErrorCounter=0
        while(True):
            time.sleep(600)#600
            try:
                print("step "+self.getCurrentTime())


                signals=self.telegram.getCurrentSignals()
                print("SIGNALS get by telegram: "+str(signals))

                #CHECK NEW ORDERS
                if(len(signals)>0):
                    qOrders=self.getQueueOrders()
                    qOrders.extend(signals)
                    self.saveQueueOrders(qOrders)
                        

                ErrorCounter=0
            except Exception as e:
                time.sleep(600)#600
                ErrorCounter+=1
                print("___________________________")
                print("ERROR EXCEPTION: "+str(e))
                print("->")
                self.telegram.reconnectToTelegram()
                print("reconnected to Telegram")
                print("___________________________")
                if ErrorCounter==20:
                    break


    def getCurrentTime(self):
        now = datetime.now()
        current_time = now.strftime("%D - %H:%M:%S")
        return str(current_time)

    def getQueueOrders(self):
        try:
            with open('Data/queuePendingSignals.json') as json_file:
                data = json.load(json_file)
                return data
        except Exception as e:
            return []

    def saveQueueOrders(self,data):
        with open('Data/queuePendingSignals.json', 'w') as outfile:
            json.dump(data, outfile)  

telegram=BotTelegram()
telegram.startBot()