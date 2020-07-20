from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer

"""
from rest_framework.decorators import api_view
@api_view(["GET"])
def list_rooms(request):
    rooms = Room.objects.all()
    serialized_rooms = RoomSerializer(rooms, many=True)
    return Response(data=serialized_rooms.data)
"""


class ListRoomsView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        # 이때 many는 True로 해야 여러 객체가 직렬화 됨
        serializer = RoomSerializer(rooms, many=True)
        # serializer 객체의 data를 Response에 담아 리턴
        return Response(serializer.data)

    def post(self, request):
        print(request.user)
        print(request.data["value"])
        print(dir(request))
        return Response()


class SeeRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    # urls.py 에서 url을 통해 받은 인자값의 변수와 일치시켜줘야 찾음.
    lookup_url_kwarg = "primary_key"
