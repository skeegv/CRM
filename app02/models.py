from django.db import models

class XXX(models.Model):
    title = models.CharField(max_length=32)


class EEE(models.Model):
    name = models.CharField(max_length=32)