import factory
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

User = get_user_model()


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.Faker("password")

    class Meta:
        model = User
