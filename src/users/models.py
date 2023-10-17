from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    User model
    """

    is_manager = models.BooleanField(default=False)
