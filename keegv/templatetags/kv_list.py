from django.template import Library
from  types import FunctionType

register = Library()


def table_head(list_display, kvadmin_obj):
    if list_display == "__all__":
        yield "对象列表"
    else:
        for item in list_display:
            if isinstance(item, FunctionType):
                # __name__ 是当前模块名,title() 方法返回'标题化'的字符串,就是说所有单词都是以大写开始，其余字母均为小写
                # header_list.append(item.__name__.title())
                yield item(kvadmin_obj, is_header=True)
            else:
                # 获取 model 里的参数( verbise_name)
                yield kvadmin_obj.model_class._meta.get_field(item).verbose_name


def table_body(result_list, list_display, kvadmin_obj):

    for row in result_list:
        if list_display == '__all__':
            yield [str(row)]
        else:
            # yield [getattr(row,name) for name in list_display]
            yield [name(kvadmin_obj, obj=row, is_header=False) if isinstance(name, FunctionType) else getattr(row, name) for name in list_display]


@register.inclusion_tag("kv/md.html")
def func(context):
    result_list = context['result_list']
    list_display = context['list_display']
    kvadmin_obj = context['kvadmin_obj']
    v = table_body(result_list, list_display, kvadmin_obj)

    h = table_head(list_display, kvadmin_obj)
    return {"result": v, 'header_list': h }


