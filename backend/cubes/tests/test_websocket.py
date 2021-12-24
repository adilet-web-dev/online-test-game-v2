import asyncio

from django.test import TestCase
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter

from cubes.routing import websocket_urlpatterns
from config.rooms import free_room_ids, closed_room_ids


application = URLRouter(websocket_urlpatterns)


class PlayerConsumerTest(TestCase):
	async def test_it_creates_connection(self):
		communicator = WebsocketCommunicator(application, "ws/games/11000&action=create")
		connected, _ = await communicator.connect()
		self.assertTrue(connected)
		await communicator.disconnect()

	async def test_it_joins_to_room(self):
		creator_communicator = WebsocketCommunicator(application, "ws/games/33000&action=create")
		player_communicator = WebsocketCommunicator(application, "ws/games/33000&action=join")

		await creator_communicator.connect()
		connected, _ = await player_communicator.connect()

		self.assertTrue(connected)

		await creator_communicator.disconnect()
		await player_communicator.disconnect()

	async def test_it_forbids_to_join_inactive_room(self):

		player_communicator = WebsocketCommunicator(application, "ws/games/44000&action=join")

		with self.assertRaises(asyncio.TimeoutError):
			connected, _ = await player_communicator.connect()

	async def test_it_forbids_to_create_busy_room(self):
		room_id = 55000
		free_room_ids.remove(room_id)
		closed_room_ids.append(room_id)
		communicator = WebsocketCommunicator(application, f"ws/games/{room_id}&action=create")

		with self.assertRaises(asyncio.TimeoutError):
			connected, _ = await communicator.connect()
