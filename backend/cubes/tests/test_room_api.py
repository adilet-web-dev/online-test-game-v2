from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from users.factories import UserFactory
from config.rooms import free_room_ids, open_room_ids, closed_room_ids


class TestRoomAPI(TestCase):
	def setUp(self) -> None:
		self.user = UserFactory()
		self.client = APIClient()
		self.client.force_login(self.user)

	def test_it_obtains_room(self):
		response = self.client.get(reverse("rooms-obtain-room"))
		self.assertIn(response.data['room_id'], free_room_ids)

	def test_it_closes_room(self):
		room_id = free_room_ids.pop(0)
		open_room_ids.append(room_id)
		self.client.post(reverse("rooms-close-room"), {
			'room_id': room_id
		})

		self.assertIn(room_id, closed_room_ids)
		self.assertNotIn(room_id, open_room_ids)
