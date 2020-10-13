from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserRegistrationSerializer


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
