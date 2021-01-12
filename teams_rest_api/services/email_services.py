import os
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.html import strip_tags

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)


TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
TEMPLATE_NAME = 'email_template.html'


class EmailServices:

    @staticmethod
    def send_verification_email(user_email, request):
        try:
            user_model = get_user_model()
            user = user_model.objects.get(email=user_email)
            # user = user_model.objects.get(id=1)
            refresh_token = str(RefreshToken.for_user(user).access_token)
            # current_site_domain = get_current_site(request).domain
            # relative_url = reverse('user-verify-email-view')
            # verify_url = f"http://{current_site_domain}{relative_url}?token={refresh_token}"
            verify_url = f"http://localhost:8080/verify?token={refresh_token}"

            mail_template = render_to_string(
                template_name=os.path.join(TEMPLATE_PATH, TEMPLATE_NAME),
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
