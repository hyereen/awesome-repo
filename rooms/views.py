from rest_framework.views import APIView
from rest_framework.response import Response # django response와 다름! 할 수 있는게 더 많다
from rest_framework import status
from .models import Room
from .serializers import ReadRoomSerializer, WriteRoomSerializer

class RoomsView(APIView):

    def get(self, request):

        rooms = Room.objects.all()
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = WriteRoomSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.create() create메소드를 직접 call하면 안돼
            room = serializer.save(user=request.user) # creat, update가 아니라 save를 call해야 함 
            room_serializer = ReadRoomSerializer(room).data
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class RoomView(APIView):

    def get(self, request, pk):
        try:
            room = Room.objects.get(pk=pk)
            serializer = ReadRoomSerializer(room).data
            return Response(serializer)
        
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def put(self, request):
        pass

    def delete(self, request):
        pass
