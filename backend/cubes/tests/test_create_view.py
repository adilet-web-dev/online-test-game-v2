from django.test import TestCase
from rest_framework.test import APIClient

from users.factories import UserFactory
from cubes.models import Test

payload = {
	'name': 'test name',
	'questions': [
		{
			'title': 'some question title',
			'options': [
				{'answer': 'option1', 'is_true': True},
				{'answer': 'option2', 'is_true': False},
				{'answer': 'option3', 'is_true': False},
				{'answer': 'option4', 'is_true': False}
			]
		}
	]
}


class TestCreateView(TestCase):
	def setUp(self) -> None:
		self.user = UserFactory()
		self.client = APIClient()
		self.client.force_login(self.user)

	def test_it_creates_test(self):
		response = self.client.post('/api/v1/tests/', payload, format="json")
		self.assertEqual(response.status_code, 201)
		self.assertTrue(Test.objects.filter(name='test name').exists())

	def test_it_forbids_non_authenticated_user(self):
		client = APIClient()
		response = client.post('/api/v1/tests/', {}, format="json")
		self.assertEqual(response.status_code, 401)
