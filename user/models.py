from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


REGISTRATION_TOKEN_LIFETIME = 1440


class RegistrationToken(models.Model):
    token = models.CharField(primary_key=True, default=uuid.uuid4(), editable=False, max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lifetime = models.IntegerField(default=REGISTRATION_TOKEN_LIFETIME)
    valid_from = models.DateTimeField(auto_now_add=True)
    valid_to = models.DateTimeField(default=timezone.now() + timezone.timedelta(seconds=REGISTRATION_TOKEN_LIFETIME))

    class Meta:
        db_table = "user_registration_token"

    def __str__(self):
        return f'{self.token})'

