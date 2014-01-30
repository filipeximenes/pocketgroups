
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from .managers import AccountManager


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=255,
        db_index=True,
        blank=True, 
        null=True
        )

    pocket_username = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        )

    pocket_access_token = models.CharField(
        max_length=255,
        db_index=True,
        blank=True,
        )

    name = models.CharField(max_length=255, blank=True)

    localizer = models.CharField(max_length=255, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'pocket_username'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name

    def __unicode__(self):
        return self.pocket_username


from django.db.models.signals import pre_save
from django.dispatch import receiver
import uuid
import base64

def get_uuid():
    r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    return r_uuid.replace('=', '')

@receiver(pre_save, sender=UserAccount)
def set_localizer_code(sender, instance, **kwargs):
    if not instance.localizer:
        instance.localizer = get_uuid()
