'''
from bithumb_machine import BithumbMachine


bithumb_machine = BithumbMachine()

#result = bithumb_machine.buy_order("BTC", 227000, 1)
#print(result)
#result = bithumb_machine.sell_order("BTC", 200000, 1)
#print(result)
ticker = bithumb_machine.get_ticker("BTC")
print(ticker['close'])
'''
import unittest
from telegram import PushTelegram

class TestSlack(unittest.TestCase):
    def setUp(self):
        self.pusher = PushTelegram()

    def test_send_message(self):
        self.pusher.send_message("RL-bot", "0.001개 코인을 매수했습니다")

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()