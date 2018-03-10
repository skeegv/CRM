from django.db import models

class XXX(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title


class EEE(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name