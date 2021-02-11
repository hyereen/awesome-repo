from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer


class ListRoomView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class SeeRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
