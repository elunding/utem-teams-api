import re

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

    VALID_EMAIL_REGEX = re.compile(r'^[A-Za-z]{3,}(\.[A-Za-z]{3,})@utem.cl$')

    email = serializers.EmailField(
        required=True,
        allow_blank=False,
    )
    password = serializers.CharField(
        min_length=8,
        max_length=64,
        allow_blank=False,
        write_only=True,
    )
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
        fields = ('email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        email = validated_data.get('email', None)
        first_name, last_name = email.split('@')[0].split('.')
        last_name = last_name[:-1]

        validated_data.update({
            'email': email.lower(),
            'first_name': first_name.lower(),
            'last_name': last_name.lower(),
        })

        user = User.objects.create_user(**validated_data)

        return user

    def validate(self, attrs):
        email = attrs.get('email', None)

        if email:
            if not self.VALID_EMAIL_REGEX.match(email):
                raise serializers.ValidationError('Invalid email address')

        return attrs
