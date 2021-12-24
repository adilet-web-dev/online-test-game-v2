from django.urls import path
from .api.views import CreateUserView


urlpatterns = [
	path("signup/<str:uuid>", CreateUserView.as_view(), name="signup")
]
