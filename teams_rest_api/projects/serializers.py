from rest_framework import serializers
from . models import (
    Project,
    Task,
)


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=True,
        max_length=100,
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
    )
    tasks = serializers.StringRelatedField(many=True)

    class Meta:
        model = Project
        fields = ['name', 'description', 'created_at', 'updated_at', 'tracks']


    def create(self, validated_data):
        """

        :param validated_data: deserialized data
        :return: new Project instance
        """
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """

        :param instance: Project instance
        :param validated_data: deserialized data
        :return: updated instance
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        return instance


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=True,
        max_length=100,
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
    )
    priority = serializers.CharField(source='get_priority_display')
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Task
