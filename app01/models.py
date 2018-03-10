from django.db import models


class UserGroup(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title


class Role(models.Model):
    name = models.CharField(verbose_name='角色', max_length=32)

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=32)
    email = models.EmailField(verbose_name="邮箱")
    ug = models.ForeignKey(UserGroup, on_delete=models.CASCADE,verbose_name="用户组", null=True, blank=True)

    def __str__(self):
        return "%s-%s" % (self.username, self.email)

    mm = models.ManyToManyField(Role, verbose_name="角色")
