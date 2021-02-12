from rest_framework.views import APIView
from rest_framework.response import Response # django response와 다름! 할 수 있는게 더 많다
from rest_framework import status
from .models import Room
from .serializers import RoomSerializer

class RoomsView(APIView):

    def get(self, request):

        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True).data
        return Response(serializer)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.create() create메소드를 직접 call하면 안돼
            room = serializer.save(user=request.user) # creat, update가 아니라 save를 call해야 함 
            room_serializer = RoomSerializer(room).data
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class RoomView(APIView):

    def get_room(self, pk):
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            return None

    def get(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            serializer = RoomSerializer(room).data
            return Response(serializer)
        
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def put(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = RoomSerializer(room, data=request.data, partial=True) 
            # 시리얼라이저에게 업데이트한다고 알려주기 위해 partial=True -> 데이터를 모두 보내는 것이 아니라 내가 바꾸고싶은 데이타만 보내는 것
            if serializer.is_valid():
                room = serializer.save()
                return Response(RoomSerializer(room).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # 에러확인
            # print(serializer.is_valid(), serializer.errors)
            return Response()
        
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        room = self.get_room(pk)
        if room.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if room is not None:
            room.delete()
            return Response(status=status.HTTP_200_OK)
        
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
