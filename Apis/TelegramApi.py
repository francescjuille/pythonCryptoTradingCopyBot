from telethon import TelegramClient, events, sync
from datetime import date
import datetime
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import dateutil, datetime, pytz
import re

#client.send_message('sddsdsdsdsss', 'n')
#client.run_until_disconnected()
"""
@client.on(events.NewMessage(chats='Joanpoool'))
async def my_event_handler(event):
    print(event.raw_text)
"""
"""
@client.on(events.NewMessage)
async def my_event_handler(event):
    if 'hello' in event.raw_text:
        await event.reply('hi!')
"""        

class TelegramApi:
    
    api_id = 'YOUR TELEGRAM KEY'
    api_hash = 'YOUR TELEGRAM KEY'
    client = TelegramClient('BOT', api_id, api_hash)

    def __init__(self):
        self.reconnectToTelegram()

    def reconnectToTelegram(self):
        self.client.start()


    def getCurrentSignals(self):
        channel_username='learn2tradectypto' # your channel
        channel_entity=self.client.get_entity(channel_username)
        posts = self.client(GetHistoryRequest(
            peer=channel_entity,
            limit=100,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0))

        signals=[]
        
        for i in posts.messages:
            #print("datetime.datetime.now(): "+str(pytz.utc.localize(datetime.datetime.now())))
            #print("i.date"+str(i.date)+" | "+str(datetime.datetime.now() - datetime.timedelta(days=1)))
            if(i.date > pytz.utc.localize(datetime.datetime.now() - datetime.timedelta(hours=2))):
                #print(str(i.message))
                #print("\n\n________________\n\n")
                resultOfSearch=None
                resultOfSearch=self.findSignalOfMessage(i.message)
                if resultOfSearch!=None:
                    signals.append(resultOfSearch)
        print("Numero de Señales: "+str(len(signals)))
        return signals     

    def findSignalOfMessage(self,message):

        r =re.compile("Trade Signal",re.IGNORECASE)
        title=r.findall(message)

        r =re.compile("rder:? (B?b?uy)",re.IGNORECASE)
        typeOrder=r.findall(message)

        r =re.compile("nstrument:? ([A-Z]{1,5})\/?USD",re.IGNORECASE)
        instrument=r.findall(message)

        r =re.compile("ntry price:? \$(\d+.\d+)",re.IGNORECASE)
        entryPrice=r.findall(message)

        r =re.compile("Stop:? \$(\d+.\d+)",re.IGNORECASE)
        stopPrice=r.findall(message)

        r =re.compile("Target:? \$(\d+.\d+)",re.IGNORECASE)
        targetPrice=r.findall(message)

        r =re.compile("Recommended Risk:? (\d+)%",re.IGNORECASE)
        recommendedRisk=r.findall(message)

        r =re.compile("[NB]?[Signal validity period]?:? ([.\d]+) h",re.IGNORECASE)
        signalTimeValidity=r.findall(message)

        #print("len(title): "+str(len(title))+", len(typeOrder): "+str(len(typeOrder))+", len(entryPrice): "+str(len(entryPrice))+", len(stopPrice): "+str(len(stopPrice))+", len(targetPrice): "+str(len(targetPrice)))
        
        if(len(title)>0 and len(typeOrder)>0 and len(entryPrice)>0 and len(stopPrice)>0 and len(targetPrice)>0):
            #print("___________")
            #print(message)
            #print("___________")
            recommendedRisk = recommendedRisk[0] if len(recommendedRisk) > 0 else None
            signalTimeValidity = signalTimeValidity[0] if len(signalTimeValidity) > 0 else 8
            signal={"instrument":instrument[0], "typeOrder": typeOrder[0], "timeSignalPublished": str(datetime.datetime.now()), "entryPrice":entryPrice[0].replace(",",""), "stopPrice":stopPrice[0].replace(",",""), "targetPrice":targetPrice[0].replace(",",""),"signalTimeValidity":signalTimeValidity}
            #print("\n_______")
            #print("SIGNAL: "+str(signal))
            #print("_______\n")
            return signal
        else:
            return None

#t=TelegramApi()
#t.getCurrentSignals()

