from channels.generic.websocket import WebsocketConsumer
import json
import subprocess
import os
import random
from time import sleep
import math

from ExchangeAPI.BithumbAPI import market_sell, market_buy, get_order_information, get_order_detail
from TestApp.models import Bot, TradeHistory
from TestApp.serializers import TradeHistorySerializer
from datetime import datetime, timezone, timedelta


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

        position = 'BUY'

        if strategyName == 'HighLowStrategy':
            highPrice = data['HighPrice']
            lowPrice = data['LowPrice']

            detail_data = None
            result = None

            while True:
                if result is not None:
                    if position == 'BUY':
                        detail_data = get_order_detail(result['order_id'], 'ask', 'BTC')

                        if detail_data['status'] != '0000':
                            sleep(60)

                            continue

                        time = datetime.fromtimestamp(int(detail_data['data'][0]['transaction_date']) / 1000000).strftime('%Y-%m-%d %H:%M:%S')

                        tradeHistoryData = {
                            'time': time,
                            'position': 'SELL',
                            'price': detail_data['data'][0]['price'],
                            'amount': detail_data['data'][0]['units_traded'],
                            'asset': asset,
                            'botId': bot.id
                        }

                        self.send(text_data=json.dumps({
                            'history': tradeHistoryData,
                            'position': position
                        }))
                    else:
                        detail_data = get_order_detail(result['order_id'], 'bid', 'BTC')

                        if detail_data['status'] != '0000':
                            sleep(60)

                            continue

                        self.send(text_data=json.dumps({
                            'detail_data': detail_data,
                            'position': position
                        }))

                        time = datetime.fromtimestamp(int(detail_data['data'][0]['transaction_date']) / 1000000).strftime('%Y-%m-%d %H:%M:%S')


                        self.send(text_data=json.dumps({
                            'time': time
                        }))

                        tradeHistoryData = {
                            'time': time,
                            'position': 'BUY',
                            'price': detail_data['data'][0]['price'],
                            'amount': detail_data['data'][0]['units_traded'],
                            'asset': asset + round(float(detail_data['data'][0]['unit_traded']) * float(detail_data['data'][0]['price']) - float(detail_data['data'][0]['fee'])),
                            'botId': bot.id
                        }

                        self.send(text_data=json.dumps({
                            'history': tradeHistoryData,
                            'position': position
                        }))

                    self.send(text_data=json.dumps({
                        'detail_data': detail_data,
                        'position': position
                    }))

                    tradeHistorySerializer = TradeHistorySerializer(data=tradeHistoryData)

                    if tradeHistorySerializer.is_valid():
                        tradeHistorySerializer.save()

                if position == 'BUY':
                    if result is None:
                        result = market_buy('BTC', math.floor((asset / lowPrice) * 10000) / 10000, lowPrice,
                                            payment_currency='KRW')
                        asset = asset - float(math.floor((asset / lowPrice) * 10000) / 10000) * lowPrice
                        print('남은 자산 : ' + str(asset))
                    else:
                        result = market_buy('BTC', math.floor(float(detail_data['data'][0]['units_traded']) * 10000) / 10000, lowPrice, payment_currency='KRW')
                        asset = asset - int(detail_data['data'][0]['total'])
                        print('남은 자산 : ' + str(asset))

                    position = 'SELL'
                else:
                    volume = math.floor(float(detail_data['data'][0]['units_traded']) * 10000) / 10000

                    result = market_sell('BTC', math.floor(float(detail_data['data'][0]['units_traded']) * 10000) / 10000, highPrice, payment_currency='BTC')
                    position = 'BUY'

                    asset = asset + round(volume * highPrice - float(detail_data['data'][0]['fee']))
                    print('자산 : ' + str(asset))

                self.send(text_data=json.dumps({
                    'result': result,
                    'position': position
                }))

                sleep(60)


class TrainConsumer(WebsocketConsumer):
    def connect(self):
        print('connect')
        self.accept()

    def disconnect(self, close_code):
        print('disconnect')

    def receive(self, text_data):
        data = json.loads(text_data)

        fromDate = data['fromDate']
        toDate = data['toDate']
        coin = data['coin']

        # self.train(fromDate, toDate, coin)

        self.send(text_data=json.dumps({
            'result': 'success'
        }))

    def train(self, fromDate, toDate, coin):
        fromDate = fromDate.split(' ')[0]
        toDate = toDate.split(' ')[0]

        train_args = ['/usr/local/bin/python3', '/Users/seungyoon-kim/Desktop/TestServer/Strategy/main.py',
                      'from=' + fromDate, 'to=' + toDate, coin]
        # train_args = ['/home/dskym0/envs/Crypstal/bin/python3', '/home/dskym0/SW_Maestro_Django/RLStrategy/main.py', 'from=' + fromDate, 'to=' + toDate, coin]
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

    def run(self, model, coin, balance):
        print(filename, coin, asset)

        run_args = ['/usr/local/bin/python3', '/Users/seungyoon-kim/Desktop/TestServer/Strategy/simulation.py',
                    'model=' + model, 'coin=' + coin, 'balance=' + balance]
        # run_args = ['/usr/local/bin/python3', '/Users/seungyoon-kim/Desktop/TestServer/Strategy/simulation.py', 'model=' + model, 'coin=' + coin, 'balance=' + balance]
        run = subprocess.Popen(run_args, stdout=subprocess.PIPE, env=os.environ.copy())

        out, err = run.communicate()
        print(out.decode('utf-8'))
