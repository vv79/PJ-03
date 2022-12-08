from django.db.models.signals import post_save
from django.dispatch import receiver
from models import RegistrationToken
from .tasks import send_post_save_registration_token_message


@receiver(post_save, sender=RegistrationToken)
def send_signup_message(sender, instance, created, **kwargs):
    send_post_save_registration_token_message.apply_async((instance.id, created))
