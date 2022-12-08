from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Response
from .tasks import send_post_save_response_message, send_post_save_response_approved_message


@receiver(post_save, sender=Response)
def send_signup_message(sender, instance, created, **kwargs):
    send_post_save_response_message.apply_async((instance.id, created))
    if instance.approved and 'approved' in kwargs['update_fields']:
        send_post_save_response_approved_message.apply_async((instance.id, created))
