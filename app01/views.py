from django.shortcuts import render,HttpResponse
from django.urls import reverse


def test(request):
    # 反向生成 URL:需要使用 namespace 做 key,因为所有程序的入口都是从这里开始有了 namespace 才能做划分.
    # 反向生成 URL:include 导入其他文件路径 include('app01.urls',namespace='aaa')
    # 反向生成功能用于,数据增删改完成之后要跳转的路径
    url = reverse('keegv:app01_userinfo_add')
    print(url)
    return HttpResponse('....')









