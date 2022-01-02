from model_bakery import baker
from django.test import TestCase
from rest_framework.test import APIClient

from cubes.models import Test
from users.factories import UserFactory


class TestListView(TestCase):
	def setUp(self) -> None:
		self.client = APIClient()
		self.user = UserFactory()
		self.client.force_login(self.user)

	def test_it_shows_test_list(self):
		baker.make(Test, 2)
		response = self.client.get('/api/v1/tests/')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), 2)
		print()

	def test_it_shows_users_own_tests(self):
		baker.make(Test, 3, author=self.user)

		response = self.client.get('/api/v1/tests/get_user_tests/')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data['tests']), 3)

