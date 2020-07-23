import jwt
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from users.models import User


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
