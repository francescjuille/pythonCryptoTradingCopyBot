import twitter


class TelegramApi:

    api=None

    def __init__(self):
        self.api = twitter.Api(consumer_key="YOUR TWITER KEY",
                        consumer_secret="YOUR TWITER KEY",
                        access_token_key="YOUR TWITER KEY",
                        access_token_secret="YOUR TWITER KEY")


    def getLastsTweetsFromUser(self,userName):
        userName="elonmusk"
        #status = api.GetUser(screen_name="elonmusk")
        results = self.api.GetUserTimeline(screen_name=userName,count=20)
        # get the text with the first character different to @     EXAMPLE: Text='RT @account: Text twit  |  Text='Text twit 

        goodResults=[]
        for i in results:
            if i.text[0]!="@":
                print("_________")
                print(i.text)
                print("_________")

        return goodResults        
