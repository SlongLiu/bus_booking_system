from django.shortcuts import render
from django.http import HttpResponseRedirect
# Create your views here.
from django.http import HttpResponse
from booking import models


def first_request(request):
    return HttpResponse('Hello world!')


def index(request):
    pass
    return render(request, 'login/index.html')


def login(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        message = "所有字段都必须填写！"
        if username and password:  # 确保用户名和密码都不为空
            username = username.strip()
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    return HttpResponseRedirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户名不存在！"
        return render(request, 'login/login.html', {"message": message})
    return render(request, 'login/login.html')


def logout(request):
    pass
    return HttpResponseRedirect('/index/')


def register(request):
    pass
    return render(request, 'login/register.html')


def base(request):
    pass
    return render(request, 'base.html')