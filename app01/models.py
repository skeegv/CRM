from django.db import models


class UserInfo(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=32)
    email = models.EmailField(verbose_name="邮箱")

    def __str__(self):
        return "%s-%s" % (self.username, self.email)


class Role(models.Model):
    name = models.CharField(verbose_name='角色', max_length=32)

    def __str__(self):
        return self.name