from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Room
from .serializers import RoomSerializer
from rest_framework.decorators import api_view

"""
@api_view(["GET", "POST"])
def list_rooms(request):
    if request.method == "GET":
        rooms = Room.objects.all()
        serialized_rooms = RoomSerializer(rooms, many=True)
        return Response(data=serialized_rooms.data)
    elif request.method == "POST":
        if request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            # room create
            room = serializer.save(user=request.user)
            room_serializer = RoomSerializer(data=room).data

            # return created object
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            # return 400 error
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""


class RoomsView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serialized_rooms = RoomSerializer(rooms, many=True)
        return Response(data=serialized_rooms.data)

    def post(self, request):
        if request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            # room create
            room = serializer.save(user=request.user)
            room_serializer = RoomSerializer(data=room).data

            # return created object
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            # return 400 error
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
            serializer = RoomSerializer(room)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            # check user
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = RoomSerializer(room, data=request.data, partial=True)
            # check data is valid
            if serializer.is_valid():
                serializer.save()
                # Response Default : HTTP_200_OK
                return Response(RoomSerializer(room).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        room = self.get_room(pk)
        # check user has room
        if room.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if room is not None:
            room.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
