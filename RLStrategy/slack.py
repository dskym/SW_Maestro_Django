from slacker import Slacker
from RLStrategy.base_pusher import Pusher
import configparser

class PushSlack(Pusher):

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        #token = config['SLACK']['token']
        token = 'xoxp-481438895186-481730301333-483207383925-890ec6c4269b14fb3fc3712f760afdba'
        self.slack = Slacker(token)

    def send_message(self, thread="#general", message=None):
        self.slack.chat.post_message(thread, message)
