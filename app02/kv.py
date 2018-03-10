from app02 import models
from keegv.service import v1
from django.urls import reverse
from django.utils.safestring import mark_safe

# 自定制类
"""
class KeegvXXX(v1.BaseKeegvAdmin):

    def func(self, obj):
        '''
        obj 当前行的对象
        return "编辑"
        return obj.title
        return "<a href='{0}'>编辑</a>".format(obj.id)
        pk = primary_key 代指数据库里的 id
        反向生成 namespace
        # name = namespace:app名称_model名称_change
        # 获取 app 名称和 模块名称 方式一
        print(self.model_class._meta.app_label)
        print(self.model_class._meta.model_name)
        # 获取 app 名称和 模块名称 方式二
        print(type(obj)._meta.app_label)
        print(type(obj)._meta.model_name)
        print(self.site.namespace)
        '''
        name = "{0}:{1}_{2}_change".format(self.site.namespace, self.model_class._meta.app_label, self.model_class._meta.model_name)

        # 反向生成 URL(args 自动把 pk 放在 \d+ 的位置)
        url = reverse(name, args=(obj.pk,))
        return mark_safe("<a href='{0}'>编辑</a>".format(url))

    def checkbox(self, obj):
        # 生 checkbox tag
        tag = "<input type='checkbox' value='{0}' />".format(obj.pk)
        return mark_safe(tag)

    # 用于显示列
    list_display = [checkbox, 'id', 'title', func]
"""

# v1.site.register(models.XXX, KeegvXXX)


# 使用默认的 BaseKeegvAdmin
v1.site.register(models.XXX)
v1.site.register(models.EEE)
