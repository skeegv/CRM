from django.db import models


class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    email = models.EmailField()

    def __str__(self):
        return "%s-%s" % (self.username, self.email)


class Role(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name