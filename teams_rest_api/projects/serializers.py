from rest_framework import serializers
from . models import (
    Project,
    Task,
)


class TaskSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        max_length=100,
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
    )
    priority = serializers.CharField(
        source='get_priority_display',
        required=False,
    )
    status = serializers.CharField(
        source='get_status_display',
        required=False,
    )

    class Meta:
        model = Task
        fields = ('name', 'description', 'priority', 'status')


class ProjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        max_length=100,
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
    )
    is_active = serializers.BooleanField(
        default=True,
    )
    tasks = TaskSerializer(
        many=True,
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Project
        fields = ('name', 'description', 'is_active', 'created_at', 'updated_at', 'tasks')

    def create(self, validated_data):
        """

        :param validated_data: deserialized data
        :return: new Project instance
        """
        tasks_data = validated_data.get('tasks', None)
        if tasks_data:
            validated_data.pop('tasks')
            project = Project.objects.create(**validated_data)
            for task_data in tasks_data:
                Task.objects.create(project=project, **task_data)
        else:
            project = Project.objects.create(**validated_data)

        return project

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
