from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .tasks import send_post_save_subscriber_messages


@receiver(post_save, sender=Post)
def send_subscribers_messages(sender, instance, created, **kwargs):
    send_post_save_subscriber_messages.apply_async((instance.id, created))
