from django.template import Library
from django.forms.models import ModelChoiceField
from django.urls import reverse
from keegv.service import v1

register = Library()


@register.inclusion_tag("kv/add_edit_form.html")
def show_add_edit_form(form):
    form_list = []
    for item in form:
        row = {'is_popup': False, 'item': None, 'popup_url': None}

        '''
        print(item.auto_id)
        
        # ModelForm 会 给每一个标签都生成一个 id. 可以通过 item.auto_id 来获取.
        id_username
        id_email
        id_ug
        id_mm
        '''

        if isinstance(item.field, ModelChoiceField) and item.field.queryset.model in v1.site._registry:
            # print(type(item.field.queryset.model._meta.app_label), item.field.queryset.model._meta.app_label, item.field.queryset.model._meta.model_name)
            target_app_label = item.field.queryset.model._meta.app_label
            target_model_name = item.field.queryset.model._meta.model_name
            # self.site.namespace
            url_name = "{0}:{1}_{2}_add".format(v1.site.namespace, target_app_label, target_model_name)

            target_url = "{0}?popup={1}".format(reverse(url_name), item.auto_id)
            '''
            print(1111111, target_url)
            
            # 带上标签 id 方便第二次发起 popup 请求的时候可以加以区分做不同的处理.
            1111111 /kv/app01/usergroup/add/?popup=id_ug
            1111111 /kv/app01/role/add/?popup=id_mm
            '''

            row['is_popup'] = True
            row['item'] = item
            row['popup_url'] = target_url
        else:
            row['item'] = item

        form_list.append(row)

    return {"form": form_list}
