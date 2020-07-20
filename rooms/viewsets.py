from rest_framework import viewsets
from .models import Room
from .serializers import BigRoomSerializer


# viewset 은 자동적으로 url을 배분함
class RoomViewset(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = BigRoomSerializer
