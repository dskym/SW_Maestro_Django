from channels.generic.websocket import WebsocketConsumer
import json
import subprocess
import os
import random
from ExchangeAPI.BithumbAPI import market_sell, market_buy, get_order_information
from TestApp.models import Bot
from time import sleep


class TradeConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)

        botId = data['botId']
        strategyName = data['name']

        bot = Bot.objects.get(id=botId)
        asset = bot.asset

        result = None
        position = 'BUY'

        if strategyName == 'HighLowStrategy':
            highPrice = data['HighPrice']
            lowPrice = data['LowPrice']

            while True:
                information = None

                if result is not None:
                    if position == 'BUY':
                        infomation = get_order_information(result['order_id'], 'ask', 'BTC')
                    else:
                        infomation = get_order_information(result['order_id'], 'bid', 'BTC')

                    if information['total'] == 'null':
                        sleep(60)

                        continue

                if position == 'BUY':
                    if result is None:
                        result = market_buy('BTC', asset / lowPrice, lowPrice, payment_currency='KRW')
                    else:
                        result = market_buy('BTC', information['units_remaining'], lowPrice, payment_currency='KRW')

                    position = 'SELL'
                else:
                    result = market_sell('BTC', result['units'], highPrice, payment_currency='BTC')
                    position = 'BUY'

                print(result)

                sleep(60)

        """
        self.send(text_data=json.dumps({
            'result': 'success'
        }))
        """


class TrainConsumer(WebsocketConsumer):
    def connect(self):
        self.num = random.randint(1, 100)
        print(self.num)
        print('connect')
        self.accept()

    def disconnect(self, close_code):
        print(self.num)
        print('disconnect')

    def receive(self, text_data):
        data = json.loads(text_data)

        fromDate = data['fromDate']
        toDate = data['toDate']
        coin = data['coin']

        #self.train(fromDate, toDate, coin)

        self.send(text_data=json.dumps({
            'result': 'success'
        }))

    def train(self, fromDate, toDate, coin):
        fromDate = fromDate.split(' ')[0]
        toDate = toDate.split(' ')[0]

        train_args = ['/usr/local/bin/python3', '/Users/seungyoon-kim/Desktop/TestServer/Strategy/main.py', 'from=' + fromDate, 'to=' + toDate, coin]
        #train_args = ['/home/dskym0/envs/Crypstal/bin/python3', '/home/dskym0/SW_Maestro_Django/RLStrategy/main.py', 'from=' + fromDate, 'to=' + toDate, coin]
        train = subprocess.Popen(train_args, stdout=subprocess.PIPE, env=os.environ.copy())

        out, err = train.communicate()
        print(out.decode('utf-8'))


class RunConsumer(WebsocketConsumer):
    def connect(self):
        print('connect')
        self.accept()

    def disconnect(self, close_code):
        print('disconnect')

    def receive(self, text_data):
        data = json.loads(text_data)

        filename = data['filename']
        asset = data['asset']
        coin = data['coin']

        """
        self.run(filename, coin, asset)

        self.send(text_data=json.dumps({
            'result': 'success'
        }))
        """

    def run(self, filename, coin, asset):
        print(filename, coin, asset)

        run_args = ['/usr/local/bin/python3', '/Users/seungyoon-kim/Desktop/TestServer/Strategy/main.py', 'filname=' + filename, 'asset=' + asset, coin]
        #run_args = ['/usr/local/bin/python3', '/Users/seungyoon-kim/Desktop/TestServer/Strategy/main.py', 'filname=' + filename, 'asset=' + asset, coin]
        run = subprocess.Popen(run_args, stdout=subprocess.PIPE, env=os.environ.copy())

        out, err = run.communicate()
        print(out.decode('utf-8'))
