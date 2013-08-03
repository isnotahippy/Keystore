from django.db import models


class KeyPair(models.Model):

    key_name = models.CharField(max_length=50)
    key_value = models.CharField(max_length=255)
