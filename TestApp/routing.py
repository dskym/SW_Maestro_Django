from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    url(r'training', consumers.TrainConsumer),
    url(r'running', consumers.RunConsumer),
]