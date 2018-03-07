from django.shortcuts import HttpResponse


class BaseKeegvAdmin(object):

    def __init__(self, model_class, site):
        self.model_class = model_class
        self.site = site


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
        from django.conf.urls import url
        ret = [
            # 启动 Django 程序就会自动生成的 URL
            # url(r'login/', self.login, name='login'),
            # url(r'logout/', self.logout, name='logout'),
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

            ret.append(url(r'%s/%s/' % (app_label, model_name), self.login))

        return ret

    @property  #@property可以把一个实例方法变成其同名属性，以支持.号访问，它亦可标记设置限制，加以规范.
    def urls(self):
        return self.get_urls(), self.app_name,self.namespace

    def login(self, request):
        return HttpResponse('login')

    def logout(self, request):
        return HttpResponse('logout')


site = Keegv()
