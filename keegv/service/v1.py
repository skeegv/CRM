from django.shortcuts import HttpResponse
from django.contrib import admin
from django.conf.urls import url, include


class BaseKeegvAdmin(object):

    def __init__(self, model_class, site):
        self.model_class = model_class
        self.site = site

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
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        data = '%s_%s_changelist' % info
        print(data)
        return HttpResponse(data)

    def add_view(self, request):
        """
        添加
        :param request: 请求信息
        :return:
        """
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        data = '%s_%s_add' % info
        print(data)
        return HttpResponse(data)

    def delete_view(self, request, pk):
        """
        删除
        :param request: 请求信息
        :param pk:  NID
        :return:
        """
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        data = '%s_%s_delete' % info
        print(data)
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
        print(data)
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

    @property  #@property可以把一个实例方法变成其同名属性，以支持.号访问，它亦可标记设置限制，加以规范.
    def urls(self):
        return self.get_urls(), self.app_name, self.namespace

    def login(self, request):
        return HttpResponse('login')

    def logout(self, request):
        return HttpResponse('logout')


site = Keegv()
