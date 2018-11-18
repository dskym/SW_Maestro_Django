from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    url(r'bot/(?P<botId>\d+)/trade', consumers.TradeConsumer),
    url(r'bot/(?P<botId>\d+)/training', consumers.TrainConsumer),
    url(r'bot/(?P<botId>\d+)/running', consumers.RunConsumer),
]