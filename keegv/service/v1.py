"""
1.数据列表页面,定制显示列

    示例1:
        v1.site.register(Model),  默认只显示对象列表

    示例2:
        class SubClass(BaseKeegvAdmin):
            list_display = []

        v1.site.register(Models, SubClass), 按照list_display 中指定的字段进行显示
        PS: 字段可以是
            - 字符串,必须是数据库里的列名
            - 函数,
                def comb(self, obj=None, is_header=False):
                    if is_header:
                        # 表头部信息
                        return "用户信息"
                    else:
                        # 表内容信息
                        return "%s-%s" %(obj.username, obj.email)



2.完整示例如下

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
"""

from django.urls import reverse
from django.shortcuts import HttpResponse, render
from django.contrib import admin
from django.conf.urls import url, include


class BaseKeegvAdmin(object):
    list_display = "__all__"
    add_or_model_form = None

    def __init__(self, model_class, site):
        self.model_class = model_class
        self.site = site
        self.request = None

        self.app_label = model_class._meta.app_label
        self.model_name = model_class._meta.model_name


    def get_add_or_model_form(self):
        if self.add_or_model_form:
            # 用户自定制配置
            return self.add_or_model_form
        else:
            # 默认配置(对象由类创建,类由 type 创建)
            from django.forms import ModelForm

            class MyModelForm(ModelForm):
                class Meta:
                    model = self.model_class
                    fields = "__all__"

            return MyModelForm

    @property
    def urls(self):
        info = self.model_class._meta.app_label, self.model_class._meta.model_name

        urlpatterns = [
            url(r'^$', self.changelist_view, name='%s_%s_changelist' % info),
            url(r'^add/$', self.add_view, name='%s_%s_add' % info),
            url(r'^(.+)/delete/$', self.delete_view, name='%s_%s_delete' % info),
            url(r'^(.+)/change/$', self.change_view, name='%s_%s_change' % info),
        ]
        return urlpatterns

    def changelist_view(self, request):
        """
        查看列表
        :param request: 请求信息
        :return:
        """
        self.request = request
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        data = '%s_%s_changelist' % info
        # print(data)
        # app01_userinfo_changelist

        result_list = self.model_class.objects.all()
        # print(self.model_class)
        # <class 'app01.models.UserInfo'>

        # 生成页面上: 添加按钮

        from django.http.request import QueryDict

        param_dict = QueryDict(mutable=True)

        if request.GET:
            # 新增一个 _changelistfilter 用来封装所有当前 request.GET 里的数据
            param_dict['_changelistfilter'] = request.GET.urlencode()

        base_add_url = reverse("{2}:{0}_{1}_add".format(self.app_label, self.model_name, self.site.namespace))

        add_url = "{0}?{1}".format(base_add_url, param_dict.urlencode())

        context = {
            'result_list': result_list,
            'list_display': self.list_display,
            'kvadmin_obj': self
        }

        return render(request, 'kv/change_list.html', {'context': context, 'add_url': add_url})

    def add_view(self, request):
        """
        添加
        :param request: 请求信息
        :return:
        """
        print(request.GET.get('_changelistfiter'))

        model_form_cls = self.get_add_or_model_form()

        context = {
            "form": model_form_cls()
        }

        return render(request, 'kv/add.html', context)

    def delete_view(self, request, pk):
        """
        删除
        :param request: 请求信息
        :param pk:  NID
        :return:
        """
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        data = '%s_%s_delete' % info

        # self.model_class.filter(id=pk).delete()
        return HttpResponse(data)

    def change_view(self, request, pk):
        """
        修改
        :param request: 请求信息
        :param pk:  nid
        :return:
        """
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        data = '%s_%s_change' % info
        return HttpResponse(data)


class Keegv(object):
    def __init__(self):
        self._registry = {}
        self.namespace = 'keegv'
        self.app_name = 'keegv'

    def register(self, model_class, xxx=BaseKeegvAdmin):
        self._registry[model_class] = xxx(model_class, self)
        """
        {
            UserInfo类: BaseKeegvAdmin(UserInfo类,Keegv对象)    # KeegvUserInfo(UserInfo类,Keegv对象)
            Role类: BaseKeegvAdmin(Role类,Keegv对象) 
            XXX类: BaseKeegvAdmin(XXX类,Keegv对象) 
        }
        """

    def get_urls(self):
        ret = [
            # 启动 Django 程序就会自动生成的 URL
            url(r'login/', self.login, name='login'),
            url(r'logout/', self.logout, name='logout'),
        ]

        # 用户通过在 app 中我们指定的文件 kv.py 中注册model ,我们会根据 model 自动生成相关的 URL
        for model_cls, keegv_admin_obj in self._registry.items():
            app_label = model_cls._meta.app_label

            model_name = model_cls._meta.model_name

            '''
            # 查看 model_cls
            print(model_cls)
            # <class 'app01.models.UserInfo'>


            # 获取 app 名称
            print(model_cls._meta.app_label)
            # app01

            # 获取 model_name
            print(model_cls._meta.model_name)
            # userinfo
            '''

            ret.append(url(r'%s/%s/' % (app_label, model_name), include(keegv_admin_obj.urls)))

        return ret

    @property  # @property可以把一个实例方法变成其同名属性，以支持.号访问，它亦可标记设置限制，加以规范.
    def urls(self):
        return self.get_urls(), self.app_name, self.namespace

    def login(self, request):
        return HttpResponse('login')

    def logout(self, request):
        return HttpResponse('logout')


site = Keegv()
