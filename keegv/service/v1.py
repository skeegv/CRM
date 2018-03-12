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
from django.shortcuts import HttpResponse, render, redirect
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
        """
        :return: MyModelForm()
        """
        if self.add_or_model_form:
            # 用户自定制配置
            return self.add_or_model_form
        else:
            # 默认配置
            from django.forms import ModelForm
            # 方式一
            # class MyModelForm(ModelForm):
            #     class Meta:
            #         model = self.model_class
            #         fields = "__all__"

            # 方式二:对象由类创建,类由 type 创建)
            _m = type('Meta', (object,), {'model': self.model_class, 'fields': "__all__"})
            MyModelForm = type('MyModelForm', (ModelForm,), {'Meta': _m})

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

        if request.method == "GET":
            model_form_obj = self.get_add_or_model_form()()
        elif request.method == "POST":
            model_form_obj = self.get_add_or_model_form()(data=request.POST, files=request.FILES)
            if model_form_obj.is_valid():
                model_form_obj.save()
                # 添加成功,进行跳转原地址
                # /kv/app01/userinfo  + request.GET.get('_changelistfiter')
                base_list_url = reverse(
                    "{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.namespace))
                list_url = "{0}?{1}".format(base_list_url, request.GET.get('_changelistfilter'))
                return redirect(list_url)

        from django.forms.boundfield import BoundField
        from django.db.models.query import QuerySet
        from django.db.models.base import ModelBase
        from django.forms.models import ModelMultipleChoiceField, ModelChoiceField

        form_list = []
        for item in model_form_obj:
            row = {'is_popup': False, 'item': None, 'popup_url': None}
            if isinstance(item.field, ModelChoiceField) and item.field.queryset.model in self.site._registry:
                # print(type(item.field.queryset.model._meta.app_label), item.field.queryset.model._meta.app_label, item.field.queryset.model._meta.model_name)
                target_app_label = item.field.queryset.model._meta.app_label
                target_model_name = item.field.queryset.model._meta.model_name
                # self.site.namespace
                url_name = "{0}:{1}_{2}_add".format(self.site.namespace, target_app_label, target_model_name)
                target_url = reverse(url_name)
                row['is_popup'] = True
                row['item'] = item
                row['popup_url'] = target_url
            else:
                row['item'] = item

            form_list.append(row)

        context = {
            "form": form_list
        }

        return render(request, 'kv/add.html', context)

    def delete_view(self, request, pk):
        """
        删除
        :param request: 请求信息
        :param pk:  NID
        :return:
        """

        """
        根据 PK 获取数据,然后 delete()
        获取 URL, 跳转会列表页面
        """
        # self.model_class.filter(id=pk).delete()
        return HttpResponse('...')

    def change_view(self, request, pk):
        """
        修改
        :param request: 请求信息
        :param pk:  nid
        :return:
        """
        # 1. 获取 _changelistfilter 中传递的参数
        # request.GET.get('_changelistfilter')
        # 2. 根据 PK 页面显示并提供默认值

        # 获取数据库对象
        obj = self.model_class.objects.filter(pk=pk).first()
        if not obj:
            return HttpResponse('ID 不存在')
        if request.method == "GET":

            model_form_obj = self.get_add_or_model_form()(instance=obj)

        else:
            # 新增数据一定要注意要添加 instance=obj, 不然就是新增一条数据.
            model_form_obj = self.get_add_or_model_form()(data=request.POST, files=request.FILES, instance=obj)
            # 验证模块
            if model_form_obj.is_valid():
                # 更新页面数据到数据
                model_form_obj.save()
                # 添加成功,进行跳转原地址
                # /kv/app01/userinfo  + request.GET.get('_changelistfiter')
                base_list_url = reverse(
                    "{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.namespace))
                list_url = "{0}?{1}".format(base_list_url, request.GET.get('_changelistfilter'))
                return redirect(list_url)
        # 3. modelForm 返回页面
        context = {
            'form': model_form_obj
        }

        return render(request, 'kv/edit.html', context)


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
