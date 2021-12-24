from rest_framework.permissions import BasePermission
from .models import Invitation


class UUIDAuthPermission(BasePermission):
	def has_permission(self, request, view):
		try:
			return Invitation.objects.filter(public_id=view.kwargs['uuid']).exists()
		except:
			return False
