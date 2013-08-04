from django.db import models
from django.contrib.auth.models import User


class KeyPair(models.Model):
    user = models.ForeignKey(User)
    key_name = models.CharField(max_length=50)
    key_value = models.CharField(max_length=255)
