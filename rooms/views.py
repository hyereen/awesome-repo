from rest_framework.views import APIView
from rest_framework.response import Response # django response와 다름! 할 수 있는게 더 많다
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from .models import Room
from .serializers import RoomSerializer

class OwnPagination(PageNumberPagination):
    page_size=20
    # 더 많이 설정하고 싶은게 있으면 넣어주면 됌 
class RoomsView(APIView):

    def get(self, request):
        #paginator = PageNumberPagination()
        #paginator.page_size = 20
        paginator = OwnPagination()
        rooms = Room.objects.all()
        results = paginator.paginate_queryset(rooms, request)
        # request를 paginator에게 파싱해준다는 것은 paginator가 page query argument를 찾아내야 한다는 것
        serializer = RoomSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data) 

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


@api_view(["GET"])
def room_search(request):
    max_price = request.GET.get('max_price', None)
    min_price = request.GET.get('min_price', None)
    beds = request.GET.get('beds', None)
    bedrooms = request.GET.get('bedrooms', None)
    bathrooms = request.GET.get('bathrooms', None)

    filter_kwargs = {}
    if max_price is not None:
        filter_kwargs["price__lte"] = max_price
    if min_price is not None:
        filter_kwargs["price__gte"] = min_price
    if beds is not None:
        filter_kwargs["beds__gte"] = beds
    if bedrooms is not None:
        filter_kwargs["bedrooms__gte"] = bedrooms
    if bathrooms is not None:
        filter_kwargs["bathrooms__gte"] = bathrooms

    paginator = PageNumberPagination()
    paginator.page_size = 10

    try:
        rooms = Room.objects.filter(**filter_kwargs)
    except ValueError: # 필터에 이상한 값을 입력한 경우
        rooms = Room.objects.all() # 모든 room을 리턴하도록 
    
    results = paginator.paginate_queryset(rooms, request)
    serializer = RoomSerializer(results, many=True)
    return paginator.get_paginated_response(serializer.data) 