from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from config.rooms import open_room_ids, closed_room_ids, free_room_ids

from cubes.models import Test
from cubes.api.serializers import TestSerializer


class TestViewSet(ModelViewSet):
	queryset = Test.objects.all()
	serializer_class = TestSerializer
	permission_classes = [IsAuthenticated]


class RoomAPIViewSet(ViewSet):

	permission_classes = [IsAuthenticated]

	@action(detail=False, methods=['GET'])
	def obtain_room(self, request):
		room_id = free_room_ids[0]
		return Response({'room_id': room_id})

	@action(detail=False, methods=['POST'])
	def close_room(self, request):
		room_id = int(request.data['room_id'])
		open_room_ids.remove(room_id)
		closed_room_ids.append(room_id)

		return Response({'message': 'ok'})
