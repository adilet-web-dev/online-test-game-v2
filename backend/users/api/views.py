from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model

from .serializers import UserSerializer
from users.permissions import UUIDAuthPermission


class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [
        AllowAny,
        UUIDAuthPermission
    ]
    serializer_class = UserSerializer
