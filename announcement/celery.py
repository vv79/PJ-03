import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsPaper.settings')

app = Celery('newsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'hello_every_5_seconds': {
        'task': 'news.tasks.hello',
        'schedule': 5
    },
    'action_every_monday_8am': {
        'task': 'news.tasks.send_cron_subscribers_messages',
        'schedule': crontab(day_of_week="mon", hour="08", minute="00"),
    }
}
