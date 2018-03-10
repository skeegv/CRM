from keegv.service import v1
from app01 import models


# class KeegvUserInfo(v1.BaseKeegvAdmin):
#     pass
# v1.site.register(models.UserInfo, KeegvUserInfo)


class KeegvUserInfo(v1.BaseKeegvAdmin):
    # 用于显示列
    list_display = ['id', 'username', 'email']


class KeegvRole(v1.BaseKeegvAdmin):
    # 用于显示列
    list_display = ['id', 'name']


v1.site.register(models.UserInfo, KeegvUserInfo)
v1.site.register(models.Role, KeegvRole)

print('keegv1')