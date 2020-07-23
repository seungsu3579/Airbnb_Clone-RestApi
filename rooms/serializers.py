from rest_framework import serializers
from .models import Room
from users.serializers import RelatedUserSerializer

"""
class RoomSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=140)
    price = serializers.IntegerField()
    bedrooms = serializers.IntegerField()
    instant_book = serializers.BooleanField()
"""


class RoomSerializer(serializers.ModelSerializer):

    user = RelatedUserSerializer()

    class Meta:
        model = Room
        exclude = ("modified",)
        read_only_fields = ("user", "id", "created", "updated")

    def validate(self, data):
        if self.instance:
            check_in = data.get("check_in", self.instance.check_in)
            check_out = data.get("check_out", self.instance.check_out)
        else:
            check_in = data.get("check_in")
            check_out = data.get("check_out")

        if check_in == check_out:
            raise serializers.ValidationError("Not enough time between changes")
        return data

    def validate_beds(self, beds):
        if beds < 2:
            raise serializers.ValidationError("Your house is too small")
