from channels.generic.websocket import WebsocketConsumer
import json
import subprocess
import os


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

        self.train(fromDate, toDate, coin)

        self.send(text_data=json.dumps({
            'result': 'success'
        }))

    def train(self, fromDate, toDate, coin):
        fromDate = fromDate.split(' ')[0]
        toDate = toDate.split(' ')[0]

        train_args = ['/usr/local/bin/python3', '/Users/seungyoon-kim/Desktop/TestServer/Strategy/main.py', 'from=' + fromDate, 'to=' + toDate, coin]
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
        run = subprocess.Popen(run_args, stdout=subprocess.PIPE, env=os.environ.copy())

        out, err = run.communicate()
        print(out.decode('utf-8'))
