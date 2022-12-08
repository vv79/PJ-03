from celery import shared_task
import time
from datetime import date, timedelta
from django.core import mail
from .models import Post, CategorySubscriber, article
from django.utils.text import Truncator
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import resolve_url


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def printer(n):
    for i in range(n):
        time.sleep(1)
        print(i+1)


@shared_task
def send_post_save_subscriber_messages(postId, created):
    instance = Post.objects.get(pk=postId)

    if instance:
        print('Sending messages to subscribers.')
        categories = instance.categories

        category_subscribers = CategorySubscriber.objects.filter(
            type=instance.type,
            category__in=categories.all()
        ).all()

        messages = []

        for category_subscriber in category_subscribers:
            user = category_subscriber.user
            if created:
                if instance.type == article:
                    subject = f'New article "{instance.title}" published.'
                else:
                    subject = f'New news "{instance.title}" published.'
            else:
                if instance.type == article:
                    subject = f'Article changed "{instance.title}".'
                else:
                    subject = f'News changed "{instance.title}".'

            context = {
                'username': user.username,
                'subject': subject,
                'content': Truncator(instance.content).chars(50),
                'url': resolve_url('article_detail', pk=instance.id) if instance.type == article else
                resolve_url('article_detail', pk=instance.id)
            }

            html_content = render_to_string('news/email/post_save_email.html', context)

            plain_message = strip_tags(html_content)

            message = mail.EmailMultiAlternatives(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email])
            message.attach_alternative(html_content, "text/html")

            messages.append(message)

        connection = mail.get_connection()
        connection.open()
        connection.send_messages(messages)
        connection.close()
    else:
        print('Post with given ID not found.')


@shared_task
def send_cron_subscribers_messages():
    messages = []
    end_date = date.today()
    start_date = end_date - timedelta(days=7)

    for category_subscriber in CategorySubscriber.objects.all():
        user = category_subscriber.user
        category = category_subscriber.category
        posts = Post.objects.filter(
            type=category_subscriber.type,
            categories__in=[category.id],
            date_created__range=[start_date, end_date]
        )

        if len(posts) > 0:
            if category_subscriber.type == article:
                subject = f'Last week articles in "{category.name}"'
            else:
                subject = f'Last week news in "{category.name}"'

            context = {
                'username': user.username,
                'subject': subject,
                'posts': posts,
                'route': 'article_detail' if category_subscriber.type == article else 'news_detail'
            }

            html_content = render_to_string('news/email/apscheduler_email.html', context)
            plain_message = strip_tags(html_content)

            message = mail.EmailMultiAlternatives(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email])
            message.attach_alternative(html_content, "text/html")

            messages.append(message)

    connection = mail.get_connection()
    connection.open()
    connection.send_messages(messages)
    connection.close()
