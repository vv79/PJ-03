import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'announcement.settings')

app = Celery('announcement')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'hello_every_1_minute': {
        'task': 'user.tasks.hello',
        'schedule': 60
    },
    'clear_old_registration_tokens_every_20_minutes': {
        'task': 'user.tasks.clear_old_registration_tokens',
        'schedule': 1440
    },
    'send_cron_subscribers_messages_every_monday_8am': {
        'task': 'board.tasks.send_cron_subscribers_messages',
        'schedule': crontab(day_of_week="thu", hour="15", minute="33"),
    }
}
