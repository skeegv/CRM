from app01 import models
from keegv.service import v1
from django.urls import reverse
from django.utils.safestring import mark_safe


# UserInfo表格显示
class KeegvUserInfo(v1.BaseKeegvAdmin):

    def func(self, obj=None, is_header=False):
        if is_header:
            return "操作"
        else:
            name = "{0}:{1}_{2}_change".format(self.site.namespace, self.model_class._meta.app_label, self.model_class._meta.model_name)
            # 反向生成 URL(args 自动把 pk 放在 \d+ 的位置)
            url = reverse(name, args=(obj.pk,))
            return mark_safe("<a href='{0}'>编辑</a>".format(url))

    def checkbox(self, obj=None, is_header=False):
        if is_header:
            # 返回页面 CheckBox 标签
            # return mark_safe('<input type="checkbox">')
            return mark_safe('选项')
        else:
            # 生 checkbox tag
            tag = "<input type='checkbox' value='{0}' />".format(obj.pk)
            return mark_safe(tag)

    def comb(self, obj=None, is_header=False):
        if is_header:
            # 表头部信息
            return "用户信息"
        else:
            # 表内容信息
            return "%s-%s" %(obj.username, obj.email)



    # 用于显示列
    list_display = [checkbox, 'id', 'username', 'email', comb,func]


v1.site.register(models.UserInfo, KeegvUserInfo)


# Role表格显示
class KeegvRole(v1.BaseKeegvAdmin):
    list_display = ['id', 'name']


v1.site.register(models.Role, KeegvRole)

