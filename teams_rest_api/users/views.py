import jwt
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
)
from services import EmailServices


logger = logging.getLogger(__name__)


class UserRegistrationView(CreateAPIView):

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                EmailServices.send_verification_email(user_email=serializer.data.get('email'))

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


class VerifyUserEmailView(APIView):

    permission_classes = (AllowAny,)

    def get(self, request):
        token = request.GET.get('token', None)

        logger.debug("verifying user...")

        if token:
            logger.debug(f"token: {token}")
            try:
                payload = jwt.decode(token, settings.SECRET_KEY)
                logger.debug(f"payload: {payload}")

                user_model = get_user_model()
                user = user_model.objects.get(id=payload['user_id'])

                logger.debug(f"user object: {user}")

                if not user.is_validated:
                    user.is_validated = True
                    user.save()

                return Response({'message': 'User succesfully activated'}, status=status.HTTP_200_OK)  # noqa

            except jwt.ExpiredSignatureError as err:
                return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)

            except jwt.exceptions.DecodeError as err:
                return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(ListAPIView):

    def get(self, request):
        user_model = get_user_model()
        authenticated_user_id = request.user.id
        users = user_model.objects.exclude(
            id=authenticated_user_id,
        ).exclude(
            first_name='',
        ).exclude(
            last_name='',
        )

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


class UserDetailView(APIView):

    def get(self, request, **kwargs):
        user_model = get_user_model()
        user_id = request.user.id
        user = get_object_or_404(user_model, pk=user_id)
        serializer = UserSerializer(user)

        return Response(serializer.data)
