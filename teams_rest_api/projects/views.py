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
            serializer.save(owner=self.request.user)
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return response


class ProjectDetailView(APIView):

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        serializer = ProjectSerializer(project)

        return Response(serializer.data)

    def put(self, request, project_id):
        import ipdb; ipdb.set_trace()
        project = get_object_or_404(Project, pk=project_id)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data)
        else:
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return response


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
                serializer.save(creator=self.request.user)
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

    def patch(self, request, task_id, project_id):
        task = get_object_or_404(Task, pk=task_id, project=project_id)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        import ipdb; ipdb.set_trace()
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data)
        else:
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return response

    def delete(self, request, task_id, project_id):
        task = get_object_or_404(Task, pk=task_id, project=project_id)
        task.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
