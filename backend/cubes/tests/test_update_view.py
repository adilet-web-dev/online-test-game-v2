from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from model_bakery import baker

from users.factories import UserFactory
from cubes.tests.test_create_view import payload
from cubes.models import Test


class TestUpdateView(TestCase):
	def setUp(self) -> None:
		self.user = UserFactory()
		self.client = APIClient()
		self.client.force_login(self.user)

	def test_it_updates_test(self):
		self.client.post('/api/v1/tests/', payload, format="json")

		test = Test.objects.get(name=payload['name'])

		payload['name'] = "new test name"
		payload['questions'][0]['title'] = "new question title"

		response = self.client.put(f'/api/v1/tests/{test.id}/', payload, format="json")

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		test.refresh_from_db()
		self.assertEqual(test.name, "new test name")
		self.assertEqual(test.questions.first().title, "new question title")

	def test_it_forbids_non_authenticated_user(self):
		test = baker.make(Test)
		client = APIClient()
		response = client.put(f'/api/v1/tests/{test.id}/', {}, format="json")
		self.assertEqual(response.status_code, 401)
