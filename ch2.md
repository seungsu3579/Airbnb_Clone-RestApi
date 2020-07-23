## :pencil2: BUILDING THE REST API

### 2.1 Create Room - part 1

- apiview 를 이용하면 django가 views를 처리하는 방식을 바꿀 수 있다.
- apiview를 사용하지 않고 function based view를 만들면 접근이 안됨.
- Serializer가 html의 form 역할을 함 > validataion check까지 가능

```python
@api_view(["GET", "POST"])
def list_rooms(request):
    if request.method == "GET":
        rooms = Room.objects.all()
        serialized_rooms = ReadRoomSerializer(rooms, many=True)
        return Response(data=serialized_rooms.data)
    elif request.method == "POST":
        serializer = WriteRoomSerializer(data=request.data)
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
```

### 2.2 Create Room - part 2

- serializer는 create, update 함수를 지원. 하지만 직접 call해서는 안됨.
- save 함수를 사용하면 직접 감지하고 알맞는 함수를 실행함.

### 2.3 Room Detail GET

- validate 함수를 serializer class에 오버라이드하여 유효성 검사를 시행할 수 있다.
- 자동적으로 validate함수가 call 되어진다.
- beds를 받으면 침대를. data를 받으면 모든 데이터를 확인

```python
def validate(self, data):
    check_in = data.get("check_in")
    check_out = data.get("check_out")
    if check_in == check_out:
        raise serializers.ValidationError("Not enough time between changes")
    else:
        return data

def validate_beds(self, beds):
    if beds < 5:
        raise serializers.ValidationError("Your house is too small")
```

### 2.4 Room Detail DELETE PUT - part 1

- DELETE

```python
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
```

### 2.5 Room Detail DELETE PUT - part 2

- UPDATE : partial=True 옵션으로 일부 인자만 받아 update가 가능함 . 디폴트는 False로 serializer는 모든 옵션을 받아야함.
- self.instance의 존재유무로만 확인 가능 > validate 함수에서 다양한

```python
# views.py
def put(self, request, pk):
    room = self.get_room(pk)
    if room is not None:
        # check user
        if room.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = WriteRoomSerializer(room, data=request.data, partial=True)
        # check data is valid
        if serializer.is_valid():
            serializer.save()
            # Response Default : HTTP_200_OK
            return Response(ReadRoomSerializer(room).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
```

- python의 get함수로 dict를 업데이트, 부족한 인자는 instance에서 기본값으로 가져올 수 있음

```python
# serializers.py
def update(self, instance, validated_data):
    instance.name = validated_data.get("name", instance.name)
    instance.address = validated_data.get("address", instance.address)
    instance.save()
    return instance
```

### 2.6 MeView and user_detail

- is_authenticated로 로그인 인증확인

```python
class MeView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            serializer = ReadUserSerializer(request.user)
            return Response(serializer.data)
        else:
            return Response({"id": "babo"})

```

### 2.7 MeView PUT

- rest_framework.permissions 의 IsAuthenticated의 permission_class 추가로 사용자 인증이 됨

- serializers.Serializer 과 serializer.ModelSerializer의 차이 : update, create를 위해 나누지 않아도 ModelSerializer가 직접 처리해준다. ( 2.4,5 에서의 문제점 해결 )

- serializer는 validate 함수를 모두 실행. 이때 validate함수는 value를 받아 리턴해야함.

### 2.8, 9 FavsView

- ModelSerializer에서 read_only_fields를 둠으로서 validate를 피할 수 있다.
- permission_classes로 user의 권한을 간단히 확인할 수 있음
- ORM many To many 관계에서 추가 및 삭제 메서드 = add(), remove()

```python
class FavsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = RoomSerializer(user.favs.all(), many=True)
        return Response(serializer.data)

    # 있으면 삭제 없으면 추가 메서드
    def put(self, request):
        pk = request.data.get("pk", None)
        user = request.user
        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response()
            except Room.DoesNotExist:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)
```

### 2.10 Creating Account

- write_only=True 옵션으로 패스워드를 안보여줄 수 있음
- password를 받아와서 기존의 create를 실행 후 Model의 내장함수인 set_password()로 패스워드를 암호화 하여 저장

```python
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = (

    def create(self, validated_data):
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
```

### 2.11 Lon In(Json Web Token)

- pyjwt 모듈을 이용하여 유저 정보를 암호화하여 전송
- BUT 누구나 JWT를 해독할 수 있음.
- JWT 장점 : 토큰에 변경사항 있는지 확인 > 매우 큰 장점이 됨

```python
import jwt
from django.conf import settings
from django.contrib.auth import authenticate

@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    # authenticate메서드는 username과 password를 받고 객체가 알맞으면 유저 객체를 반환
    user = authenticate(username=username, password=password)
    print(user)
    if user is not None:
        # 암호키를 settings.py에 있는 키를 씀.
        encoded_jwt = jwt.encode(
            {"id": user.pk}, settings.SECRET_KEY, algorithm="HS256"
        )
        return Response(data={"token": encoded_jwt})
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
```

### 2.12 JWT Decoding and Auth

- settings.py에 직접 커스텀한 JWT인증을 추가한다.
- request.META에서 토큰을 받아와 디코딩을 진행 후 유저 객체를 리턴

```python
# settings.py
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "config.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
}

# authentication.py
class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # username = request.META.get('HTTP_X_USERNAME')
        try:
            token = request.META.get("HTTP_AUTHORIZATION")
            if token is None:
                return None
            else:
                xjwt, jwt_token = token.split(" ")
                decoded = jwt.decode(
                    jwt_token, settings.SECRET_KEY, algorithms=["HS256"]
                )
                print(decoded)
                pk = decoded.get("pk")
                print(pk)
                user = User.objects.get(pk=pk)
                return (user, None)
        except (ValueError, jwt.exceptions.DecodeError, User.DoesNotExist):
            return None
```

### 2.13 JWT Recap

- login : 토큰을 만듬
  -- username, password를 받아와서 로그인
  -- jwt를 encode하여 토큰을 만들어 리턴
- settings.py에 인증방법 추가 : API가 authorization header를 이해하게 해야함.
  -- request.META로 부터 token을 받아서 decode
  -- 토큰 안의 정보로 user 객체를 찾음
  -- 객체를 리턴
  -- ( 다양한 인증 방법을 장고 rest framework가 제공 )
  -- ( jwt는 db에 저장 안됨, 장고에서 제공하는 토큰은 db에 저장되서 migration 필수 )
