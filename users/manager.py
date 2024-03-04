from django.contrib.auth.models import BaseUserManager
from models import CustomUser

class CustomUserManager(BaseUserManager):
    def create_user(self, username, display_name, from_42=True, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, display_name=display_name, from_42=from_42, **extra_fields)
        user.save(using=self._db)
        return user
