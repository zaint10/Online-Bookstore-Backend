from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class UserRegisterSerializer(serializers.Serializer):
    """
    Serializer for user registration.
    """
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)

class UserLogoutSerializer(serializers.Serializer):
    """
    Serializer for user logout.
    """
    pass


class EmailAuthTokenSerializer(serializers.Serializer):
    """
    Serializer for obtaining authentication token using email.
    """
    email = serializers.EmailField(label="Email")
    password = serializers.CharField(
        label="Password", style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        """
        Validate email and password.
        """
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(request=self.context.get("request"), email=email, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
