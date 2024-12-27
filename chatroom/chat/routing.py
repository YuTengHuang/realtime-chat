from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat_rooms/', ChatConsumer.as_asgi()),
]