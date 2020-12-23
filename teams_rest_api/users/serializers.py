from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(required=True)
    first_name = serializers.CharField(
        required=False,
        max_length=50,
    )
    last_name = serializers.CharField(
        required=False,
        max_length=50,
    )

    class Meta:
        model = User
        fields = ('uuid', 'first_name', 'last_name')

    def to_representation(self, obj):
        return {
            'full_name': f'{obj.first_name} {obj.last_name}',
            'uuid': obj.uuid,
        }


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
