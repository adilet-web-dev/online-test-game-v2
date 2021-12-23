from django.urls import path
from . import consumers


websocket_urlpatterns = [
	path('ws/games/<int:room_id>&action=<str:command>', consumers.PlayerConsumer.as_asgi(), name='game')
]
