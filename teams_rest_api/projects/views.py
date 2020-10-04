from django.http.response import JsonResponse
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


class ProjectCreateView(APIView):

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return response


class ProjectDetailView(APIView):

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        serializer = ProjectSerializer(project)

        return Response(serializer.data)


class TaskListView(APIView):

    def get(self, request, **kwargs):
        project_id = kwargs.get('project_id', None)
        tasks = Task.objects.filter(project=project_id).all()
        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data)


class TaskCreateView(APIView):

    def post(self, request, **kwargs):
        project_id = kwargs.get('project_id', None)
        if project_id:
            request.data.update({
                'project': project_id,
            })
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return response


class TaskDetailView(APIView):

    def get(self, request, task_id, project_id):
        task = get_object_or_404(Task, pk=task_id, project=project_id)
        serializer = TaskSerializer(task)

        return Response(serializer.data)
