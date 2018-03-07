from keegv.service import v1
from app01 import models


# class KeegvUserInfo(v1.BaseKeegvAdmin):
#     pass
# v1.site.register(models.UserInfo, KeegvUserInfo)


v1.site.register(models.UserInfo)
v1.site.register(models.Role)

print('keegv1')