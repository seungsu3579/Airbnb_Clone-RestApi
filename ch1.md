## :pencil2: CH1. INTRODUCTION TO DRF

### 1.1 @api_view

- function base view
  api_view가 가이드라인이 되며 http method를 request.method로 확인안해도 됨!

```python
@api_view(["GET"])
def list_rooms(request):
    rooms = Room.objects.all()
    serialized_rooms = RoomSerializer(rooms, many=True)
    return Response(data=serialized_rooms.data)
```

### 1.2 Serializers - part1

파이썬 객체를 JSON 객체로 변환 또는 그 반대

- serializers.Serializer : model이 아닌 것을 serialize할 때 유용함

```python
class RoomSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=140)
    price = serializers.IntegerField()
    bedrooms = serializers.IntegerField()
    instant_book = serializers.BooleanField()
```

### 1.3 Serializers - part2

- serializers.ModelSerializer : model을 serialize 해줌
  serializer에 다른 serializer를 포함하면 relation까지 표현 가능

```python
class RoomSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer()
    class Meta:
        model = Room
        fields = ("name", "price", "bedrooms", "instant_book", "user")
```

### 1.4 Class Based Views

- APIView 를 상속 받아 Class view를 구현

```python
from rest_framework.views import APIView

class ListRoomsView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
```

- pagination :
  `#PageNumberPagination` `#LimitOffsetPagination`
  `#CursorPagination` `#Custom Pagination`

```python
# settings.py : Django Page
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}
```

### 1.5 ListAPIView

- ListAPIView 를 상속 받으면 더 간단히 가능
  많은 것을 커스터마이징할 필요가 없을 때(인증이 불가...)
  <a href="cdrf.co">django_rest_framework_doc1</a>
  <a href="ccbv.co.uk">django_rest_framework_doc2</a>

```python
# urls.py
urlpatterns = [
    path("<int:primary_key>/", views.SeeRoomView.as_view()),
]

# views.py
from rest_framework.generics import ListAPIView

class SeeRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = BigRoomSerializer
    # urls.py 에서 url을 통해 받은 인자값의 변수와 일치시켜줘야 찾음.
    lookup_url_kwarg = "primary_key"
```

### 1.6 ModelViewSet

- CRUD를 한번에 처리. GET POST DELETE PUT 모두 세팅되어 있음
  즉, 자유도가 떨어져 논리를 추가할 수 없음.

```python
# urls.py
from rest_framework.routers import DefaultRouter
from . import viewsets

router = DefaultRouter()
router.register("", viewsets.RoomViewset, basename="room")
urlpatterns = router.urls

# views.py
from rest_framework import viewsets
# viewset 은 자동적으로 url을 배분함
class RoomViewset(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = BigRoomSerializer
```
