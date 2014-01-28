
from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, pocket_username, password=None):
        if not pocket_username:
            msg = 'Users must have an username address'
            raise ValueError(msg)

        user = self.model(
            pocket_username=pocket_username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, pocket_username, password):
        user = self.create_user(pocket_username,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
