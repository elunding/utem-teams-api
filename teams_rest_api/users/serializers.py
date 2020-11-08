from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        required=True,
        max_length=50,
    )
    last_name = serializers.CharField(
        required=True,
        max_length=50,
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        min_length=8,
        max_length=64,
    )
    first_name = serializers.CharField(
        required=True,
        max_length=50,
    )
    last_name = serializers.CharField(
        required=True,
        max_length=50,
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user
