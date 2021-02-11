from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Room

class RoomSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    class Meta:
        model = Room
        # 포함된걸 쓰고싶을 떄 
        # fields = ("pk", "name", "price", "user")
        # 전체에서 포함하지 않는 걸 적고 싶을 떄
        exclude = ("modified",)
