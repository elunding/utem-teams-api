from django.shortcuts import (
    render,
    get_object_or_404,
)
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
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
from users.serializers import UserSerializer


class ProjectListView(APIView):

    def get(self, request):


        projects = Project.objects.filter(project_members=request.user)
        if projects:
            serializer = ProjectSerializer(projects, many=True)
            response_data = serializer.data

            for project in response_data:
                is_owned_by_user = bool(project['owner']['full_name'] == str(request.user))
                project['is_owned_by_user'] = is_owned_by_user

                # finished_tasks = [task for task in project['tasks'] if task['status'] == 'DN']  # noqa
                # finished_tasks_percentage = (len(finished_tasks) / len(response_data[0]['tasks'])) * 100  # noqa

            # import ipdb; ipdb.set_trace()
            status_code = status.HTTP_200_OK

        else:
            response_data = 'Not found'
            status_code = status.HTTP_404_NOT_FOUND

        response = {
            'data': response_data,
            'status_code': status_code,
        }

        return Response(response, status_code)


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

    def patch(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        serializer = ProjectSerializer(project, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data)
        else:
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return response


class TaskListView(ListAPIView):

    model = Task
    serializer_class = TaskSerializer

    def get(self, request, **kwargs):
        project_id = kwargs.get('project_id', None)
        tasks = Task.objects.filter(project=project_id).all()
        if tasks:
            todo_tasks = tasks.filter(
                project=project_id,
                status='TD',
            ).all()

            in_progress_tasks = tasks.filter(
                project=project_id,
                status='IP',
            ).all()

            done_tasks = tasks.filter(
                project=project_id,
                status='DN',
            ).all()

            serialized_todo_tasks = self.serializer_class(todo_tasks, many=True).data
            serialized_in_progress_tasks = self.serializer_class(in_progress_tasks, many=True).data
            serialized_done_tasks = self.serializer_class(done_tasks, many=True).data
            project_name = Project.objects.get(id=project_id).name

            response_data = {
                'todo_tasks': serialized_todo_tasks,
                'in_progress_tasks': serialized_in_progress_tasks,
                'done_tasks': serialized_done_tasks,
                'project_name': project_name,
            }
            status_code = status.HTTP_200_OK
        else:
            response_data = 'Not found'
            status_code = status.HTTP_404_NOT_FOUND

        response = {
            'data': response_data,
            'status_code': status_code,
        }

        return Response(response, status_code)


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


class MemberListView(ListAPIView):
    def get(self, request, **kwargs):
        project_id = kwargs.get('project_id', None)
        members = Project.objects.get(id=project_id).project_members.all()

        if members:
            serializer = UserSerializer(members, many=True)
            response_data = serializer.data
            status_code = status.HTTP_200_OK
        else:
            response_data = 'Not found'
            status_code = status.HTTP_404_NOT_FOUND

        response = {
            'data': response_data,
            'status_code': status_code,
        }

        return Response(response, status_code)
