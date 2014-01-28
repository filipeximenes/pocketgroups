
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from .managers import AccountManager


class UserAccount(AbstractBaseUser, PermissionsMixin):
    # email = models.EmailField(
    #     max_length=255,
    #     unique=True,
    #     db_index=True,
    #     required=False
    #     )

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


