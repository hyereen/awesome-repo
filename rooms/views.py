from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet # viewset
from rest_framework.response import Response # django response와 다름! 할 수 있는게 더 많다
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from .models import Room
from .serializers import RoomSerializer
from .permissions import IsOwner


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):

        if self.action == "list" or self.action == "retrieve": # /rooms GET or /room/1/ GET
            permission_classes = [permissions.AllowAny] # 누구나 요청할 수 있도록 허용
        elif self.action == "create": # 방 만들기
            permission_classes = [permissions.IsAuthenticated] # 인증받은 유저만 가능
        else: # 이 외 모든 경우
            # 우리만의 permission을 넣어야 함, 우리가 원하는 permission을 제공하지 않아서 만들어야 됨
            # DELETE /rooms/1/ PUT /rooms/1/
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes] # 들여쓰기 주의,,ㅠㅠ
            # permission class를 리턴할 순 없음 
            # permission을 호출할건데 대상은 permission_classes에 있는 모든 permission


@api_view(["GET"])
def room_search(request):
    max_price = request.GET.get("max_price", None)
    min_price = request.GET.get("min_price", None)
    beds = request.GET.get("beds", None)
    bedrooms = request.GET.get("bedrooms", None)
    bathrooms = request.GET.get("bathrooms", None)
    lat = request.GET.get("lat", None)
    lng = request.GET.get("lng", None)

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

    if lat is not None and lng is not None:
        filter_kwargs["lat__gte"] = float(lat) - 0.005
        filter_kwargs["lat__lte"] = float(lat) + 0.005
        filter_kwargs["lng__gte"] = float(lng) - 0.005
        filter_kwargs["lng__lte"] = float(lng) + 0.005


    try:
        rooms = Room.objects.filter(**filter_kwargs)
    except ValueError: # 필터에 이상한 값을 입력한 경우
        rooms = Room.objects.all() # 모든 room을 리턴하도록 
    
    results = paginator.paginate_queryset(rooms, request)
    serializer = RoomSerializer(results, many=True)
    return paginator.get_paginated_response(serializer.data) 