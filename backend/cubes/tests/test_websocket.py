import asyncio

from django.test import TestCase
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter

from cubes.routing import websocket_urlpatterns
from config.rooms import free_room_ids, open_room_ids, closed_room_ids


application = URLRouter(websocket_urlpatterns)


class CreatorConsumerTest(TestCase):
	async def test_it_creates_connection(self):
		communicator = WebsocketCommunicator(application, "ws/cubes/11000/creator")
		connected, _ = await communicator.connect()
		self.assertTrue(connected)

		await communicator.disconnect()

	async def test_it_sends_message_to_player(self):
		room_id = 44444

		creator_communicator = WebsocketCommunicator(application, f"ws/cubes/{room_id}/creator")
		player_communicator = WebsocketCommunicator(application, f"ws/cubes/{room_id}/player")

		await creator_communicator.connect()
		await player_communicator.connect()

		await creator_communicator.send_to(text_data="something")
		event = await player_communicator.receive_output(timeout=2)
		self.assertEqual(event['text'], 'something')

	async def test_it_forbids_to_create_closed_room(self):
		room_id = 55000
		free_room_ids.remove(room_id)
		closed_room_ids.append(room_id)
		communicator = WebsocketCommunicator(application, f"ws/cubes/{room_id}/creator")

		with self.assertRaises(asyncio.TimeoutError):
			connected, _ = await communicator.connect()


class PlayerConsumerTest(TestCase):
	async def test_it_joins_to_room(self):

		room_id = 33000
		player_communicator = WebsocketCommunicator(application, f"ws/cubes/{room_id}/player")
		open_room_ids.append(room_id)

		connected, _ = await player_communicator.connect()
		self.assertTrue(connected)

		await player_communicator.disconnect()

	async def test_it_sends_message_to_creator(self):
		room_id = 33333
		creator_communicator = WebsocketCommunicator(application, f"ws/cubes/{room_id}/creator")
		player_communicator = WebsocketCommunicator(application, f"ws/cubes/{room_id}/player")

		await creator_communicator.connect()
		await player_communicator.connect()

		await player_communicator.send_to(text_data="something")
		event = await creator_communicator.receive_output(timeout=2)
		self.assertEqual(event['text'], 'something')

	async def test_it_forbids_to_join_inactive_room(self):

		player_communicator = WebsocketCommunicator(application, "ws/cubes/44000/player")

		with self.assertRaises(asyncio.TimeoutError):
			connected, _ = await player_communicator.connect()
