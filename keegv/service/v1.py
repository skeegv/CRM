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


site = Keegv()
