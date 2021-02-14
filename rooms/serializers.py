from rest_framework import serializers
from users.serializers import RelatedUserSerializer
from .models import Room

class RoomSerializer(serializers.ModelSerializer):

    user = RelatedUserSerializer()
    is_fav = serializers.SerializerMethodField()

    class Meta:
        model = Room
        exclude = ("modified",)

        # 새로운 room을 create할때나 update할 때 user validate하면 안돼
        # list를 create하면 돼 read-only list
        read_only_fields = ("user", "id", "created", "updated")

    def validate(self, data):
        # 업데이트 하는 경우 
        if self.instance:
            check_in = data.get('check_in', self.instance.check_in) # , 뒤의 값은 default값
            check_out = data.get('check_out', self.instance.check_out)
        else: # create하는 경우
            check_in = data.get('check_in')
            check_out = data.get('check_out')
            if check_in == check_out:
                raise serializers.ValidationError("Not enough time between changes")

        return data #반드시!

    def get_is_fav(self, obj):
        # self는 serializer, obj는 현재 처리되고 있는 room
        request = self.context.get("request")
        if request:
            user = request.user
            if user.is_authenticated:
                return obj in user.favs.all() #user.favs.all()는 배열 
                # 1 in [1,2,3] 이어서 그 결과가 True인지 False인지 알 수 있게됨 
        return False
