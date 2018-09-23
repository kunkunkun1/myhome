from django.shortcuts import render, redirect,HttpResponse
from django.views import View

from dbmodels.models import ShowImg, RightNav, Menu, Transaction
from django.contrib.auth import authenticate, login as lgi, logout as lgt
import functools

# Create your views here.
def index(request):
    # 返回图片

    slider = ShowImg.objects.get_slider()
    right_nav = RightNav.objects.get_title()
    if request.session.get('menu') is None:
        menu = Menu.objects.get_menu()
        request.session['menu'] = menu

    return render(request, 'index.html', {'slider': slider,
                                          'right_nav': right_nav,
                                          })


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        rember = request.POST.get('rember')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            lgi(request, user)
            if not rember:
                request.session.set_expiry(0)
            return redirect('web:index')

    return render(request, 'login.html')


def logout(request):
    lgt(request)
    return redirect('web:login')

def transaction_deal(func):
    @functools.wraps(func)
    def warp(*args,**kwargs):
        new_kwargs = {}
        for i,j in kwargs.items():
            if j:
                new_kwargs[i] = int(j[:-1])

        args = args + (1,) if new_kwargs.get('pk') else args + (0,)

        result = func(*args,**new_kwargs)
        return result
    return warp


@transaction_deal
def transaction(request,*args,**kwargs):
    if request.method == 'GET' and not args[-1]:
        result_list = Transaction.objects.get_transaction(**kwargs)
        return render(request, 'list.html', {
            'result_list': result_list,
        })
    else:
        pass




def user(request):
    # data = Transaction.objects.all()

    from django.http import JsonResponse
    # from django.core import serializers
    #
    # data1 = serializers.serialize('json',data)
    # print(data1)
    # print(Transaction.objects.values())
    result = JsonResponse(list(Transaction.objects.values()),safe=False)
    print(result)
    return result

