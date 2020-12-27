from django.contrib.auth import get_user_model
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
)


class UserRegistrationView(CreateAPIView):

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                response = Response(
                    {
                        'message': 'User registration successful',
                        'success': True,
                    },
                    status=status.HTTP_201_CREATED,
                )

            else:
                response = Response(
                    {
                        'error': serializer.errors,
                        'success': False,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            response = Response(
                {
                    'error': str(e),
                    'success': False,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return response


class UserListView(ListAPIView):

    def get(self, request):
        user_model = get_user_model()
        users = user_model.objects.all()

        response_data = 'Not found'
        status_code = status.HTTP_404_NOT_FOUND

        if users:
            serializer = UserSerializer(users, many=True)
            response_data = serializer.data
            status_code = status.HTTP_200_OK

        response = {
            'data': response_data,
            'status_code': status_code,
        }

        return Response(response, status_code)
