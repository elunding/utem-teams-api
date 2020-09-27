from django.shortcuts import (
    render,
    get_object_or_404,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import (
    Task,
    Project,
)

from .serializers import (
    TaskSerializer,
    ProjectSerializer,
)


class ProjectListView(APIView):

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)

        return Response(serializer.data)


class ProjectDetailView(APIView):

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        serializer = ProjectSerializer(project)

        return Response(serializer.data)


class TaskListView(APIView):

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data)


class TaskDetailView(APIView):

    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        serializer = TaskSerializer(task)

        return Response(serializer.data)
