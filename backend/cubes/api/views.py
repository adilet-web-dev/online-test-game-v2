from random import randint

from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from config.rooms import open_room_ids, closed_room_ids, free_room_ids

from cubes.models import Test
from cubes.api.serializers import TestSerializer


class TestViewSet(ModelViewSet):
	queryset = Test.objects.all()
	serializer_class = TestSerializer
	permission_classes = [IsAuthenticated]

	def create(self, request, *args, **kwargs):
		serializer = TestSerializer(
			data=request.data,
			context={'user': request.user}
		)

		serializer.is_valid(raise_exception=True)
		serializer.save()
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

	@action(detail=False, methods=['GET'])
	def get_user_tests(self, request):
		tests = self.get_queryset()
		serializer = TestSerializer(tests.filter(author=request.user), many=True)
		return Response(serializer.data)

	@action(detail=True, methods=['GET'])
	def check_owner(self, request, pk=None):
		test = self.get_object()
		return Response(test.author == request.user)


class RoomAPIViewSet(ViewSet):

	permission_classes = [IsAuthenticated]

	@action(detail=False, methods=['GET'])
	def obtain_room(self, request):
		room_id = free_room_ids[randint(0, len(free_room_ids)-1)]
		return Response({'room_id': room_id})

	@action(detail=False, methods=['POST'])
	def close_room(self, request):
		room_id = int(request.data['room_id'])
		open_room_ids.remove(room_id)
		closed_room_ids.append(room_id)

		return Response({'message': 'ok'})
