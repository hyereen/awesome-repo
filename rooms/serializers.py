from rest_framework import serializers
from users.serializers import RelatedUserSerializer
from .models import Room

class RoomSerializer(serializers.ModelSerializer):

    user = RelatedUserSerializer()
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
