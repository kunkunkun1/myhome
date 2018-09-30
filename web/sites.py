from collections import OrderedDict

from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import AlreadyRegistered, AdminSite
from django.contrib.admin.templatetags.admin_list import _coerce_field_name
from django.contrib.admin.utils import label_for_field, quote
from django.core.exceptions import FieldDoesNotExist
from django.db.models.expressions import OrderBy, F
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from django.views.decorators.cache import never_cache
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login as lgi, logout as lgt
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
import importlib
from dbmodels.models import ShowImg, RightNav, Menu, Transaction
from django.utils.html import format_html






class MyModelAdmin(ModelAdmin):
    list_template_name = "list.html"
    detail_template_name = "detail.html"
    create_template_name = "create.html"
    update_template_name = "create.html"
    delete_template_name = None



    def get_urls(self):
        from django.urls import path

        info = self.opts.model_name

        urlpatterns = [
            path('', self.changelist_view, name='%s_changelist' % info),
            path('add/', self.add_view, name='%s_add' % info),
            path('<path:object_id>/delete/', self.delete_view, name='%s_delete' % info),
            path('<path:object_id>/change/', self.change_view, name='%s_change' % info),
            path('<path:object_id>/detail/', self.detail_view, name='%s_detail' % info),
        ]
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls()

    def _get_view_cls(self, method, extra_pro=None):
        cls_name = '%s%sView' % (self.opts.model_name, method)

        module = importlib.import_module('django.views.generic')
        father_cls = getattr(module, '%sView' % method.capitalize())

        cls_pro = {
            'template_name': getattr(self, '%s_template_name' % method),
            'model': self.model,
        }
        cls_pro.update(extra_pro or {})

        cls = type(cls_name, (father_cls,), cls_pro)
        return cls

    def _has_extra_pro_method(self, method,extra_context = None):
        '''返回额外的类属性和方法'''
        m = '%s_extra_pro' % method
        extra_context = extra_context or {}
        if hasattr(self, m):
            d = getattr(self, m)()
            d.update({'extra_context':extra_context})
            return d

    def changelist_view(self, request,extra_context=None):
        template_response = super(MyModelAdmin,self).changelist_view(request,extra_context)

        cl = template_response.context_data['cl']
        def url_for_result(cl, result):
            pk = getattr(result, cl.pk_attname)
            return reverse('web:%s_change' % cl.opts.model_name,
                           args=(quote(pk),),
                           current_app=cl.model_admin.admin_site.name)

        from functools import partial
        cl.url_for_result = partial(url_for_result,cl)

        method = 'list'

        extra_pro = self._has_extra_pro_method(method,template_response.context_data)

        cls = self._get_view_cls(method, extra_pro)

        return cls.as_view()(request)

    def add_view(self, request,  form_url='', extra_context=None):
        method = 'create'

        extra_pro = self._has_extra_pro_method(method)

        cls = self._get_view_cls(method, extra_pro)

        return cls.as_view()(request)

    def change_view(self, request, object_id,form_url='', extra_context=None ):
        method = 'update'

        kwargs = {'pk': object_id}

        extra_pro = self._has_extra_pro_method(method)

        cls = self._get_view_cls(method, extra_pro)
        return cls.as_view()(request, **kwargs)

    def delete_view(self, request, object_id, extra_context=None):
        method = 'delete'

        kwargs = {'pk': object_id}

        extra_pro = self._has_extra_pro_method(method)

        cls = self._get_view_cls(method, extra_pro)
        return cls.as_view()(request, **kwargs)

    def detail_view(self, request, object_id, ):
        method = 'detail'

        kwargs = {'pk': object_id}

        extra_pro = self._has_extra_pro_method(method)

        cls = self._get_view_cls(method, extra_pro)
        return cls.as_view()(request, **kwargs)





class WebSite(AdminSite):

    def get_urls(self):
        from django.urls import include, path

        urlpatterns = [
            path('', self.index, name='index'),
            path('login/', self.login, name='login'),
            path('logout/', self.logout, name='logout'),
            path('jsi18n/', self.i18n_javascript, name='jsi18n'),
        ]

        for model, model_admin in self._registry.items():
            urlpatterns += [
                path('%s/' % (model._meta.model_name), include(model_admin.urls)),
            ]

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'web', self.name

    @never_cache
    def index(self, request, extra_context=None):

        slider = ShowImg.objects.get_slider()
        right_nav = RightNav.objects.get_title()
        if request.session.get('menu') is None:
            menu = Menu.objects.get_menu()
            request.session['menu'] = menu

        context = {'slider': slider,
                   'right_nav': right_nav}

        context.update(extra_context or {})

        return render(request, 'index.html', context)

    @never_cache
    def logout(self, request):
        lgt(request)
        return redirect('web:login')

    @never_cache
    def login(self, request,):
        return LoginView.as_view()(request)


class LoginView(View):
    def valid_user(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        return user

    def post(self, request, *args, **kwargs):
        user = self.valid_user(request)
        if user is not None:
            lgi(request, user)
            rember = request.POST.get('rember')
            if not rember:
                request.session.set_expiry(0)
            return redirect('web:index')
        self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')


class ChangeListView(ListView):
    template_name = "list.html"
    model = Transaction
    ordering = ('-create_time')
    context_object_name = 'result_list'


class WebDetailView(DetailView):
    template_name = "detail.html"
    model = Transaction


class AddView(CreateView):
    template_name = "create.html"
    model = Transaction
    fields = '__all__'

    # success_url = reverse
    def get_success_url(self):
        return reverse('web:transaction_changelist')

    extra_context = None
    def get_context_data(self):
        pass


class WebUpdateView(UpdateView):
    template_name = "create.html"
    model = Transaction
    fields = '__all__'

    def get_success_url(self):
        return reverse('web:transaction_changelist')


class WebDeleteView(DeleteView):
    model = Transaction

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('web:transaction_changelist')


class TModelAdmin(MyModelAdmin):
    list_display = ('__str__', 'team', 'img', 'stat', 'user','get_btn')
    list_editable = ('team', 'img', 'stat', 'user',)

    def get_btn(self,obj):
        s = '''  <a href="{}" class="btn-link">
                    <span class="label label-info">查看</span>
                </a>
                <a href="{}" class="btn-link">
                    <span class="label label-success">修改</span>
                </a>
                <a href="{}" class="btn-link">
                    <span class="label label-warning">删除</span>
                </a>'''
        return format_html(
            s,
             reverse('web:transaction_detail',args=(obj.pk,)),
             reverse('web:transaction_change',args=(obj.pk,)),
             reverse('web:transaction_delete',args=(obj.pk,)),

        )
    get_btn.short_description = '操作'

    def list_extra_pro(self):
        return {# 'context_object_name': 'result_list',
                #'extra_context': self.get_list_extra_context,
                }

    def create_extra_pro(self):
        return {'get_success_url': self.get_success_url,
                'fields': '__all__',
                'extra_context':self.get_create_extra_context,
                }

    def update_extra_pro(self):
        return {'get_success_url': self.get_success_url,
                'fields': '__all__',}

    def delete_extra_pro(self):
        return {'get_success_url': self.get_success_url,
                'get': self.get}

    @staticmethod
    def get_success_url(self):
        return reverse('web:transaction_changelist')

    @staticmethod
    def get(self, request, *args, **kwargs):
        return getattr(self, 'post')(request, *args, **kwargs)

    @property
    def get_uptdate_fields(self):
        fields = '__all__'
        return fields

    @property
    def get_create_fields(self):
        fields = '__all__'
        return fields

    @property
    def get_create_extra_context(self):
        '''add_view 展示的页面的context'''
        return {'s1':'5'}

    # @property
    # def get_list_extra_context(self):
    #     '''add_view 展示的页面的context'''
    #     from django.contrib.admin.templatetags import admin_list
    #     return {'result_list_ccc':admin_list.result_list(self.cl)}
site = WebSite(name='web')
site.register(Transaction, TModelAdmin)
