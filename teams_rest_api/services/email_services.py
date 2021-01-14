import os
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.html import strip_tags

from rest_framework_simplejwt.tokens import RefreshToken
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)


TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
VERIFY_EMAIL_TEMPLATE = 'email_template.html'
INVITATION_EMAIL_TEMPLATE = 'invitation_email_template.html'


class EmailServices:

    @staticmethod
    def send_verification_email(user_email):
        try:
            user_model = get_user_model()
            user = user_model.objects.get(email=user_email)
            refresh_token = str(RefreshToken.for_user(user).access_token)
            verify_url = f"http://localhost:8080/verify?token={refresh_token}"

            mail_template = render_to_string(
                template_name=os.path.join(TEMPLATE_PATH, VERIFY_EMAIL_TEMPLATE),
                context={
                    'first_name': user.first_name,
                    'url': verify_url,
                },
            )

            send_mail(
                subject='Verifica tu cuenta',
                message=strip_tags(mail_template),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user_email, 'esteban.lundin@gmail.com'],
                html_message=mail_template,
            )

        except Exception as e:
            logger.debug(f"An error has occurred: {e}", exc_info=True)
            raise e


    @staticmethod
    def send_project_invitation(invited_user_email, project_name, project_owner_name, invitation_id):  # noqa
        try:
            # for user_email in invited_user_emails:
            user_model = get_user_model()
            user = user_model.objects.get(email=invited_user_email)
            # refresh_token = str(RefreshToken.for_user(user).access_token)
            join_project_url = f"http://localhost:8080/join_project?invitation={invitation_id}"  # noqa

            mail_template = render_to_string(
                template_name=os.path.join(TEMPLATE_PATH, INVITATION_EMAIL_TEMPLATE),
                context={
                    'first_name': user.first_name,
                    'project_owner_name': project_owner_name,
                    'project_name': project_name,
                    'url': join_project_url,
                },
            )

            send_mail(
                subject=f"Invitación a {project_name}",
                message=strip_tags(mail_template),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[invited_user_email, 'esteban.lundin@gmail.com'],
                html_message=mail_template,
            )

        except Exception as e:
            logger.debug(f"An error has occurred: {e}", exc_info=True)
            raise e
