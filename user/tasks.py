from celery import shared_task
from django.utils import timezone
import logging
from django.core import mail
from .models import RegistrationToken
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import resolve_url


@shared_task
def hello():
    print("Hello, world!")

@shared_task
def clear_old_registration_tokens():
    registration_tokens = RegistrationToken.objects.filter(valid_to_lt=timezone.now())
    for registration_token in registration_tokens:
        registration_token.delete()


@shared_task
def send_post_save_registration_token_message(tokenId, created):
    registration_token = RegistrationToken.objects.get(pk=tokenId)

    if registration_token:
        if not registration_token.expired:
            messages = []

            user = registration_token.user
            subject = 'Welcome to announcement board.'

            context = {
                'username': user.username,
                'subject': subject,
                'confirmation_url': resolve_url('confirm_registration', token=registration_token.token)
            }

            html_content = render_to_string('user/email/user_registered.html', context)

            plain_message = strip_tags(html_content)

            message = mail.EmailMultiAlternatives(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email])
            message.attach_alternative(html_content, "text/html")

            messages.append(message)

            connection = mail.get_connection()
            connection.open()
            connection.send_messages(messages)
            connection.close()
        else:
            logging.log(logging.INFO, f'Registration token with ID {tokenId} is expired and will be removed.')
            registration_token.delete()

    else:
        logging.log(logging.ERROR, f'Registration token with ID {tokenId} not found.')

