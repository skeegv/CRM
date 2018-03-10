from django.template import Library
from  types import FunctionType

register = Library()


def table_head(arg):
    pass


def table_body(result_list, list_display, kvadmin_obj):
    for row in result_list:
        # yield [getattr(row,name) for name in list_display]
        yield [name(kvadmin_obj, row) if isinstance(name, FunctionType) else getattr(row, name) for name in list_display]


@register.inclusion_tag("kv/md.html")
def func(context):
    result_list = context['result_list']
    list_display = context['list_display']
    kvadmin_obj = context['kvadmin_obj']
    v = table_body(result_list, list_display, kvadmin_obj)

    for item in list_display:
        print(item, kvadmin_obj.model_class)
        if isinstance(item, FunctionType):
            print(item.__name__.title())
        else:
            print(item)
    return {"result": v}
