from rest_framework import serializers
from users.serializers import RelatedUserSerializer
from .models import Room

class ReadRoomSerializer(serializers.ModelSerializer):

    user = RelatedUserSerializer()
    class Meta:
        model = Room
        exclude = ("modified",)

class WriteRoomSerializer(serializers.Serializer):
    
    name = serializers.CharField(max_length=140)
    address = serializers.CharField(max_length=140)
    price = serializers.IntegerField()
    beds = serializers.IntegerField(default=1)
    lat = serializers.DecimalField(max_digits=10, decimal_places=6)
    lng = serializers.DecimalField(max_digits=10, decimal_places=6)
    bedrooms = serializers.IntegerField(default=1)
    bathrooms = serializers.IntegerField(default=1)
    check_in = serializers.TimeField(default="00:00:00")
    check_out = serializers.TimeField(default="00:00:00")
    instant_book = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return Room.objects.create(**validated_data) # 반드시 리턴해줘야 함 

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

    def update(self, instance, validated_data):
        # 업데이트 하고 싶은게 일부일 수 있으니까 그거의 validation을 다 해줘야 됨
        instance.name = validated_data.get("name", instance.name)
        instance.address = validated_data.get("address", instance.address)
        instance.price = validated_data.get("price", instance.price)
        instance.beds = validated_data.get("beds", instance.beds)
        instance.lat = validated_data.get("lat", instance.lat)
        instance.lng = validated_data.get("lng", instance.lng)
        instance.bedrooms = validated_data.get("bedrooms", instance.bedrooms)
        instance.bathrooms = validated_data.get("bathrooms", instance.bathrooms)
        instance.check_in = validated_data.get("check_in", instance.check_in)
        instance.check_out = validated_data.get("check_out", instance.check_out)
        instance.instant_book = validated_data.get("instant_book", instance.instant_book)

        instance.save()

        return instance