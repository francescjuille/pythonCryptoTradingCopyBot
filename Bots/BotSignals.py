import sys
sys.path.append(".")
import time, json
from datetime import datetime, timedelta
import threading
from Binance.config import clientBinance as BINANCE
from Binance.config import reconnectToBinance

from Binance.Account import Account
from Binance.Orders import Orders
from Binance.CryptoInfo import CryptoInfo

"""
Simple bot that execute signals
"""

class BotTelegram:

    cryptoInfo=CryptoInfo()
    orders=Orders()
    account=Account()

    def __init__(self):
        pass

    def startBot(self):
        print("SIGNALS BOT STARTED")
        ErrorCounter=0
        while(True):
            time.sleep(100)#100
            try:
                print("step "+self.getCurrentTime())

                newSignals=self.getQueueOrders()
                self.saveQueueOrders([])

                orders=self.getOrders()

                #CHECK NEW ORDERS
                if(len(newSignals)>0):
                    for newSignal in newSignals:
                        if(self.checkIfOrderAlreadyExists(newSignal)==False and self.cryptoInfo.getSimbolPrice(newSignal["instrument"]+"USDT")!=None):
                            newSignal["status"]="waiting"
                            orders.append(newSignal)
                            self.saveOrder(newSignal)
                            print("order saved: "+str(newSignal))
                self.saveOrder(orders)
                
                #TESTING MODE
                #break
                #



                #CHECK RUNNING ORDERS
                print("\nCHECK RUNNING ORDERS")
                index=0
                indexToDelete=[]                
                for order in orders:

                    try:
                        if(order["simpleOrder"]=="SIMPLE"):
                            if(order["typeOrder"].upper().strip()=="SELL"):
                                self.buyOrder(order)
                            else:
                                self.sellOrder(order)
                            orders[index]["status"]="target"   
                            indexToDelete.append(index)
                    except:
                        pass


                    if(order["status"]=="target" or order["status"]=="signalTimeOut" or order["status"]=="stop" or (self.isOrderTimeout(order) and order["status"]=="waiting")):
                        print("borrar element")
                        if(order["status"]=="waiting"):
                            orders[index]["status"]="signalTimeOut"
                        indexToDelete.append(index)
                    else:
                        targetPrice=order["targetPrice"]
                        stopPrice=order["stopPrice"]
                        entryPrice=order["entryPrice"]
                        actualPrice=self.cryptoInfo.getSimbolPrice(order["instrument"]+"USDT")

                        print("float(actualPrice)>float(entryPrice): "+str(float(actualPrice))+" > "+str(float(entryPrice)))
                        print("float(actualPrice)<float(stopPrice): "+str(float(actualPrice))+" < "+str(float(stopPrice)))

                        if (float(actualPrice)>float(entryPrice) and order["status"]=="waiting"):
                            print("time to buy")
                            result=self.buyOrder(order)
                            orders[index]["status"]="running"
                            orders[index]["orderId"]=result["orderId"]

                        if (float(actualPrice)>float(targetPrice)):
                            print("target arrived")
                            if(orders[index]["status"]=="running"):
                                self.sellOrder(order)
                            orders[index]["status"]="target"

                        if (float(actualPrice)<float(stopPrice)):
                            print("stop arrived")
                            if(orders[index]["status"]=="running"):
                                self.sellOrder(order)
                            orders[index]["status"]="stop"   

                    index+=1
                self.saveOrder(orders)       


                ErrorCounter=0
            except Exception as e:
                time.sleep(500)#500
                ErrorCounter+=1
                print("___________________________")
                print("ERROR EXCEPTION: "+str(e))
                print("->")
                reconnectToBinance()
                #self.telegram.reconnectToTelegram()
                print("reconnected to Binance")
                print("___________________________")
                if ErrorCounter==20:
                    break


    def buyOrder(self,order):
        symbol=order["instrument"]+"USDT"
        price=self.cryptoInfo.getSimbolPrice(symbol)
        PERCENTATGE_OF_ACCOUNT_FOR_OPERATION=30
        quantity=((self.account.getTotalMoneyInWallet("USDT")/(100/PERCENTATGE_OF_ACCOUNT_FOR_OPERATION)) * (1/price))
        print("BUY")
        print("price: "+str(price))
        print("quantiti: "+str(quantity))
        print("__________")
        return self.orders.createOrder(self.symbol,quantity,price,BINANCE.SIDE_BUY,marketPrice=True)

    def sellOrder(self,order):
        price=self.cryptoInfo.getSimbolPrice(order["instrument"]+"USDT")
        quantity=self.account.getTotalMoneyInWallet(order["instrument"])
        print("SELL")
        print("price: "+str(price))
        print("quantiti: "+str(quantity))
        print("___________")
        return self.orders.createOrder(self.symbol,quantity,price,BINANCE.SIDE_SELL,marketPrice=True)    

    def isOrderTimeout(self, order):
        if(datetime.now() < datetime.strptime(order["timeSignalPublished"], '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=order["signalTimeValidity"])):
            return False
        return True


    def saveOrder(self,data):
        #check if object type is array, if not, convert it
        if str(type(data)).replace("list","")==str(type(data)):
            data=[data]
        with open('Data/signals.json', 'w') as outfile:
            json.dump(data, outfile)

    def getOrders(self):
        try:
            with open('Data/signals.json') as json_file:
                data = json.load(json_file)
                return data
        except:
            return []

    def getQueueOrders(self):
        try:
            with open('Data/queuePendingSignals.json') as json_file:
                data = json.load(json_file)
                return data
        except:
            return []

    def saveQueueOrders(self,data):
        with open('Data/queuePendingSignals.json', 'w') as outfile:
            json.dump(data, outfile)             



    def checkIfOrderAlreadyExists(self,newOrder):
        oldOrders=self.getOrders()
        print("CHECK oldOrders: "+str(oldOrders))
        print("newOrder: "+str(newOrder))
        for order in oldOrders:
            if(order["instrument"]==newOrder["instrument"] and order["entryPrice"]==newOrder["entryPrice"] and order["stopPrice"]==newOrder["stopPrice"] and order["targetPrice"]==newOrder["targetPrice"]):
                return True
        return False        

    def getCurrentTime(self):
        now = datetime.now()
        current_time = now.strftime("%D - %H:%M:%S")
        return str(current_time)



telegram=BotTelegram()
telegram.startBot()