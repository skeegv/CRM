from django.apps import AppConfig


# 定制启动文件
class KeegvConfig(AppConfig):
    name = 'keegv'
    # Django 程序启动时会第一时间执行每一个 APP 里的 apps.py 文件
    def ready(self):
        super(KeegvConfig, self).ready()
        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('kv')