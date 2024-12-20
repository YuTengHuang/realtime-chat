from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import RoomSerializer
from .models import Room


class RoomView(GenericAPIView):

    serializer_class = RoomSerializer
    def get(self, request):
        rooms = Room.objects.get_all_rooms(request.user)
        serializer = self.serializer_class(rooms, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)