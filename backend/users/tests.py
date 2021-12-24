from django.test import TestCase
from django.shortcuts import reverse
from model_bakery import baker

from users.factories import UserFactory
from .models import Invitation


# Create your tests here.
class TestSignUp(TestCase):
	def test_it_creates_account_by_invitation(self):
		invitation = baker.make(Invitation)
		response = self.client.post(reverse("signup", args=[invitation.public_id]), {
			"username": "test_username",
			"password": "some123password456"
		})

		self.assertEqual(response.status_code, 201)

	def test_it_forbids_create_existing_account(self):
		invitation = baker.make(Invitation)
		user = UserFactory()
		response = self.client.post(reverse("signup", args=[invitation.public_id]), {
			"username": user.username,
			"password": user.password
		})

		self.assertEqual(response.status_code, 400)

	def test_it_cannot_use_invitation_twice(self):
		invitation = baker.make(Invitation)
		user = UserFactory()
		self.client.post(reverse("signup", args=[invitation.public_id]), {
			"username": user.username,
			"password": user.password
		})

		user2 = UserFactory()
		response = self.client.post(reverse("signup", args=[invitation.public_id]), {
			"username": user2.username,
			"password": user2.password
		})

		self.assertEqual(response.status_code, 401)

	def test_it_does_not_create_account_by_wrong_invitation(self):
		public_id = "gfaskjajkr4k7r3ark8a32g23872k3"
		response = self.client.post(reverse("signup", args=[public_id]), {
			"username": "test_username",
			"password": "some123password456"
		})

		self.assertEqual(response.status_code, 401)
