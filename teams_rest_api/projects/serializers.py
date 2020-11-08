from collections import OrderedDict
from rest_framework import serializers

from users.serializers import UserSerializer
from users.models import User

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
        read_only=True,
    )
    owner = UserSerializer(read_only=True)
    project_members = UserSerializer(
        many=True,
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Project
        fields = ('name', 'description', 'is_active', 'created_at', 'updated_at', 'tasks', 'owner', 'project_members')  # noqa

    def create(self, validated_data):
        """

        :param validated_data: deserialized data
        :return: new Project instance
        """
        members_data = validated_data.get('project_members', None)
        owner = validated_data['owner']
        owner_details = OrderedDict(
            [
                ('uuid', owner.uuid),
                ('first_name', owner.first_name),
                ('last_name', owner.last_name),
            ],
        )
        members_data.append(owner_details)

        if members_data:
            del validated_data['project_members']
            project = Project.objects.create(**validated_data)

            for member_data in members_data:
                user_record = User.objects.filter(**member_data).first()

                if user_record:
                    user_record.contributing_projects.add(project)

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
