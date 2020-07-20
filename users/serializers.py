from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        # 배제할 field
        exclude = (
            "groups",
            "password",
            "user_permissions",
            "last_login",
            "is_superuser",
            "is_active",
            "date_joined",
            "favs",
        )
