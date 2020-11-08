from collections import OrderedDict
from rest_framework import serializers

from users.serializers import UserSerializer
from users.models import User

from . models import (
    Project,
    Task,
)


class TaskSerializer(serializers.ModelSerializer):
    PRIORITY_CHOICES = (
        (1, 'LOW'),
        (2, 'MEDIUM'),
        (3, 'HIGH'),
    )

    STATUS_CHOICES = (
        ('TD', 'TODO'),
        ('IP', 'IN_PROGRESS'),
        ('DN', 'DONE'),
    )

    name = serializers.CharField(
        required=True,
        max_length=100,
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=500,
    )
    priority = serializers.ChoiceField(
        choices=PRIORITY_CHOICES,
        required=False,
    )
    priority_name = serializers.SerializerMethodField(
        read_only=True,
        source='get_priority_name',
    )
    status = serializers.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
    )
    status_name = serializers.SerializerMethodField(
        read_only=True,
        source='get_status_name',
    )
    project = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Project.objects.all(),
    )
    assignee = UserSerializer(required=False)
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('name', 'description', 'priority', 'priority_name', 'status', 'status_name', 'project', 'created_at', 'updated_at', 'assignee', 'creator')  # noqa

    def get_priority_name(self, obj):
        return obj.get_priority_display()

    def get_status_name(self, obj):
        return obj.get_status_display()

    def create(self, validated_data):
        """
        :param validated_data: deserialized data
        :return: new Task instance
        """
        assignee_data = validated_data.get('assignee', None)

        if assignee_data:
            del validated_data['assignee']
            task = Task.objects.create(**validated_data)
            assignee_record = User.objects.filter(**assignee_data).first()

            if assignee_record:
                assignee_record.assigned_tasks.add(task)

        else:
            task = Task.objects.create(**validated_data)

        return task

    def update(self, instance, validated_data):
        """

        :param instance: Task instance
        :param validated_data: deserialized data
        :return: updated Task instance
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.status = validated_data.get('status', instance.status)
        instance.assignee = validated_data.get('assignee', instance.assignee)
        instance.save()

        return instance


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
        owner = validated_data.get('owner', None)
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
        :return: updated Project instance
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()

        return instance
