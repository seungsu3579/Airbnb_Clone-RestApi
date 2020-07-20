import json
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse
from rooms.models import Room


def list_rooms(request):

    """
    rooms = Room.objects.all()
    rooms_json = []
    for room in rooms:
        # dumps : 객체를 json 포맷으로 나열
        rooms_json.append(json.dumps(room))
    # query set을 json으로 변환하기 위해 serialize 필요
    response = HttpResponse(content=rooms_json)
    """

    # 하지만 일반적인 방법으로 X   >  장고는 serializers를 동반함
    data = serializers.serialize("json", Room.objects.all())
    response = HttpResponse(content=data)

    return response
