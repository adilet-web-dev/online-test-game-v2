from django.urls import path
from cubes.consumers import PlayerConsumer, CreatorConsumer


websocket_urlpatterns = [
	path('ws/cubes/<int:room_id>/creator', CreatorConsumer.as_asgi(), name='creator'),
	path('ws/cubes/<int:room_id>/player', PlayerConsumer.as_asgi(), name='player')
]
