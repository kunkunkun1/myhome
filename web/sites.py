from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.admin.templatetags.admin_list import _coerce_field_name
from django.contrib.admin.utils import label_for_field
from django.utils.safestring import mark_safe
from django.views.decorators.cache import never_cache
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login as lgi, logout as lgt
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
import importlib
from dbmodels.models import ShowImg, RightNav, Menu, Transaction
from django.utils.html import format_html
ALL_VAR = 'all'
ORDER_VAR = 'o'
ORDER_TYPE_VAR = 'ot'
PAGE_VAR = 'p'
SEARCH_VAR = 'q'
ERROR_FLAG = 'e'

IS_POPUP_VAR = '_popup'
TO_FIELD_VAR = '_to_field'


HORIZONTAL, VERTICAL = 1, 2


IGNORED_PARAMS = (
    ALL_VAR, ORDER_VAR, ORDER_TYPE_VAR, SEARCH_VAR, IS_POPUP_VAR, TO_FIELD_VAR)




class ModelAdmin:
    list_template_name = "list.html"
    detail_template_name = "detail.html"
    create_template_name = "create.html"
    update_template_name = "create.html"
    delete_template_name = None
    fields = '__all__'

    list_display = ('__str__')
    list_display_links =()
    date_hierarchy = None
    list_per_page = None
    list_max_show_all = None
    list_editable = None

    def __init__(self, model, web_site):
        self.model = model
        self.opts = model._meta
        self.web_site = web_site

    def get_urls(self):
        from django.urls import path

        info = self.opts.model_name

        urlpatterns = [
            path('', self.changelist_view, name='%s_changelist' % info),
            path('add/', self.create_view, name='%s_add' % info),
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
            'fields': self.fields
        }
        cls_pro.update(extra_pro or {})

        cls = type(cls_name, (father_cls,), cls_pro)
        return cls

    def _has_extra_pro_method(self, method):
        '''返回额外的类属性和方法'''
        m = '%s_extra_pro' % method
        if hasattr(self, m):
            return getattr(self, m)()



    def get_changelist_instance(self,request):
        list_display = self.get_list_display(request)
        list_display_links = self.get_list_display_links(request, list_display)
        # Add the action checkboxes if any actions are available.
        # if self.get_actions(request):
        #     list_display = ['action_checkbox'] + list(list_display)
        ChangeList = self.get_changelist(request)
        return ChangeList(
            request,
            self.model,
            list_display,
            list_display_links,
        )

    def changelist_view(self, request, ):
        method = 'list'

        cl = self.get_changelist_instance(request)

        extra_pro = self._has_extra_pro_method(method)

        cls = self._get_view_cls(method, extra_pro)


        return cls.as_view()(request)

    def create_view(self, request, ):
        method = 'create'

        extra_pro = self._has_extra_pro_method(method)

        cls = self._get_view_cls(method, extra_pro)

        return cls.as_view()(request)

    def change_view(self, request, object_id, ):
        method = 'update'

        kwargs = {'pk': object_id}

        extra_pro = self._has_extra_pro_method(method)

        cls = self._get_view_cls(method, extra_pro)
        return cls.as_view()(request, **kwargs)

    def delete_view(self, request, object_id, ):
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

    def get_list_display(self, request):
        return self.list_display

    def get_list_display_links(self, request, list_display):
        return self.list_display_links

    def get_changelist(self, request):
        return ChangeList

    def get_list_filter(self, request):
        pass

    def get_search_fields(self, request):
        pass

    def get_list_select_related(self, request):
        pass

class ChangeList:
    def __init__(self, request, model, list_display, list_display_links,model_admin):
        self.model = model
        self.opts = model._meta
        self.lookup_opts = self.opts

        self.list_display = list_display
        self.list_display_links = list_display_links

        self.model_admin = model_admin

    def result_headers(self):
        """
        Generate the list column headers.
        """
        ordering_field_columns = self.get_ordering_field_columns()
        for i, field_name in enumerate(self.list_display):
            text, attr = label_for_field(
                field_name, self.model,
                model_admin=self.model_admin,
                return_attr=True
            )
            if attr:
                field_name = _coerce_field_name(field_name, i)
                # Potentially not sortable

                # if the field is the action checkbox: no sorting and special class
                if field_name == 'action_checkbox':
                    yield {
                        "text": text,
                        "class_attrib": mark_safe(' class="action-checkbox-column"'),
                        "sortable": False,
                    }
                    continue

                admin_order_field = getattr(attr, "admin_order_field", None)
                if not admin_order_field:
                    # Not sortable
                    yield {
                        "text": text,
                        "class_attrib": format_html(' class="column-{}"', field_name),
                        "sortable": False,
                    }
                    continue

            # OK, it is sortable if we got this far
            th_classes = ['sortable', 'column-{}'.format(field_name)]
            order_type = ''
            new_order_type = 'asc'
            sort_priority = 0
            sorted = False
            # Is it currently being sorted on?
            if i in ordering_field_columns:
                sorted = True
                order_type = ordering_field_columns.get(i).lower()
                sort_priority = list(ordering_field_columns).index(i) + 1
                th_classes.append('sorted %sending' % order_type)
                new_order_type = {'asc': 'desc', 'desc': 'asc'}[order_type]

            # build new ordering param
            o_list_primary = []  # URL for making this field the primary sort
            o_list_remove = []  # URL for removing this field from sort
            o_list_toggle = []  # URL for toggling order type for this field

            def make_qs_param(t, n):
                return ('-' if t == 'desc' else '') + str(n)

            for j, ot in ordering_field_columns.items():
                if j == i:  # Same column
                    param = make_qs_param(new_order_type, j)
                    # We want clicking on this header to bring the ordering to the
                    # front
                    o_list_primary.insert(0, param)
                    o_list_toggle.append(param)
                    # o_list_remove - omit
                else:
                    param = make_qs_param(ot, j)
                    o_list_primary.append(param)
                    o_list_toggle.append(param)
                    o_list_remove.append(param)

            if i not in ordering_field_columns:
                o_list_primary.insert(0, make_qs_param(new_order_type, i))

            yield {
                "text": text,
                "sortable": True,
                "sorted": sorted,
                "ascending": order_type == "asc",
                "sort_priority": sort_priority,
                "url_primary": self.get_query_string({ORDER_VAR: '.'.join(o_list_primary)}),
                "url_remove": self.get_query_string({ORDER_VAR: '.'.join(o_list_remove)}),
                "url_toggle": self.get_query_string({ORDER_VAR: '.'.join(o_list_toggle)}),
                "class_attrib": format_html(' class="{}"', ' '.join(th_classes)) if th_classes else '',
            }

    def result_hidden_fields(self):
        pass

    def results(self):
        pass

    def result_list(self):

        headers = list(self.result_headers())
        num_sorted_fields = 0
        for h in headers:
            if h['sortable'] and h['sorted']:
                num_sorted_fields += 1
        return {'cl': self,
                'result_hidden_fields': list(self.result_hidden_fields()),
                'result_headers': headers,
                'num_sorted_fields': num_sorted_fields,
                'results': list(self.results())}




class WebSite:
    _empty_value_display = '-'

    def __init__(self, name='web'):
        self._registry = {}  # model_class class -> admin_class instance
        self.name = name

    def register(self, model, admin_class=None,):

        if not admin_class:
            admin_class = ModelAdmin

        if model in self._registry:
            raise AlreadyRegistered('The model %s is already registered' % model.__name__)

        self._registry[model] = admin_class(model, self)

    def get_urls(self):
        from django.urls import include, path

        urlpatterns = [
            path('', self.index, name='index'),
            path('login/', self.login, name='login'),
            path('logout/', self.logout, name='logout'),
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


class TModelAdmin(ModelAdmin):
    def list_extra_pro(self):
        return {'context_object_name': 'result_list'}

    def create_extra_pro(self):
        return {'get_success_url': self.get_success_url}

    def update_extra_pro(self):
        return {'get_success_url': self.get_success_url}

    def delete_extra_pro(self):
        return {'get_success_url': self.get_success_url,
                'get': self.get}

    @staticmethod
    def get_success_url(self):
        return reverse('web:transaction_changelist')

    @staticmethod
    def get(self, request, *args, **kwargs):
        return getattr(self, 'post')(request, *args, **kwargs)


site = WebSite()
site.register(Transaction, TModelAdmin)
