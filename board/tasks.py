from celery import shared_task
from datetime import date, timedelta
import logging
from django.core import mail
from .models import Announcement, Response, CategorySubscriber
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import resolve_url


@shared_task
def send_post_save_response_message(responseId, created):
    response = Response.objects.get(pk=responseId)

    if response:
        messages = []

        announcement = response.announcement
        user = announcement.author
        subject = 'Response was added to your announcement.'

        context = {
            'username': user.username,
            'subject': subject,
            'response_url': resolve_url('response_detail', pk=response.id)
        }

        html_content = render_to_string('board/email/response_created.html', context)

        plain_message = strip_tags(html_content)

        message = mail.EmailMultiAlternatives(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email])
        message.attach_alternative(html_content, "text/html")

        messages.append(message)

        connection = mail.get_connection()
        connection.open()
        connection.send_messages(messages)
        connection.close()

    else:
        logging.log(logging.ERROR, f'Response with ID {responseId} not found.')


@shared_task
def send_cron_subscribers_messages():
    messages = []
    end_date = date.today()
    start_date = end_date - timedelta(days=7)

    for category_subscriber in CategorySubscriber.objects.all():
        user = category_subscriber.user
        category = category_subscriber.category
        announcements = Announcement.objects.filter(
            category__in=[category.id],
            date_created__range=[start_date, end_date]
        )

        if len(announcements) > 0:
            subject = f'Last week announcements in "{category.name}"'

            context = {
                'username': user.username,
                'subject': subject,
                'announcements': announcements,
                'route': 'announcement_detail'
            }

            html_content = render_to_string('board/email/cron_subscriber_message.html', context)
            plain_message = strip_tags(html_content)

            message = mail.EmailMultiAlternatives(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email])
            message.attach_alternative(html_content, "text/html")

            messages.append(message)

    connection = mail.get_connection()
    connection.open()
    connection.send_messages(messages)
    connection.close()


@shared_task
def send_post_save_response_approved_message(responseId, created):
    response = Response.objects.get(pk=responseId)

    if response:
        messages = []

        announcement = response.announcement
        user = announcement.user
        subject = 'Your response was approved.'

        context = {
            'username': user.username,
            'subject': subject,
            'response_url': resolve_url('response_detail', pk=response.id)
        }

        html_content = render_to_string('board/email/response_approved.html', context)

        plain_message = strip_tags(html_content)

        message = mail.EmailMultiAlternatives(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email])
        message.attach_alternative(html_content, "text/html")

        messages.append(message)

        connection = mail.get_connection()
        connection.open()
        connection.send_messages(messages)
        connection.close()

    else:
        logging.log(logging.ERROR, f'Response with ID {responseId} not found.')