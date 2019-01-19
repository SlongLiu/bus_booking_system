from django.http import HttpResponseRedirect
# Create your views here.
from django.http import HttpResponse
from booking import models
from django.shortcuts import render, redirect
from .forms import UserForm, RegisterForm
import hashlib
from django.forms.models import model_to_dict
import datetime


def hash_code(s, salt='ojbk'):
    h = hashlib.sha3_256()
    s += salt
    h.update(s.encode())
    # print('h=', h.hexdigest())
    return h.hexdigest()


def first_request(request):
    return HttpResponse('Hello world!')


def index(request):
    pass
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = '请检查填写的内容'
        if login_form.is_valid():
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['identify'] = user.identify
                    print(user.identify)
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户名不存在！"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")

    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            # print(register_form.cleaned_data['mobile'])
            mobile = register_form.cleaned_data['mobile']
            realname = register_form.cleaned_data['realname']
            identify = register_form.cleaned_data['identify']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())

                same_mobile_user = models.User.objects.filter(name=mobile)
                if same_mobile_user: # 手机号唯一
                    message = '该手机号已被注册，请登录或者重新输入'
                    return render(request, 'login/register.html', locals())

                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # print('完成检验 可以注册')
                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.realname = realname
                new_user.mobile = mobile
                new_user.identify = identify
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面

    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def base(request):
    pass
    return render(request, 'base.html')


def browse(request):
    '''
    进入预定页面，返回所有线路的信息
    :param request:
    :return:
    '''

    lines = models.Line.objects.all()
    # print('lines=', model_to_dict(lines[0]))
    # print('time', str(model_to_dict(lines[0])['service_time_start']).split()[0])
    # l1 = models.Line.objects.get(name=lines[0])
    # print('l1=', l1)

    context = []

    for item in lines:
        # print(item)
        item_dict = model_to_dict(item)
        line_price = models.PriceOfLine.objects.filter(line_id=str(item_dict['id']))
        # 构建各车站票价列表
        price = [model_to_dict(x) for x in line_price]
        item_dict['price'] = price
        # print(item_dict)

        # 构建发车时间的list
        timetable = []
        i = item_dict['service_time_start']
        interval = item_dict['interval']
        while (1) :
            # print(i > item_dict['service_time_end'])
            # print(i > item_dict['service_time_start'])
            if (item_dict['service_time_start'] < item_dict['service_time_end']):

                if ((i>item_dict['service_time_end']) and (i>item_dict['service_time_start'])) \
                        or((i<item_dict['service_time_end']) and (i<item_dict['service_time_start'])):
                    # print('---------------')
                    break
            else:
                if ((i>item_dict['service_time_end']) and (i<item_dict['service_time_start'])):
                    # print('---------------')
                    break

            timetable.append(i)
            print(i)
            i = datetime.time((i.hour+interval.hour + (i.minute+interval.minute) // 60) % 24, \
                              (i.minute+interval.minute) % 60)
        print(timetable)
        item_dict['timetable'] = timetable
        context.append(item_dict)

    return render(request, 'booking/browse.html', {
        'num': len(context),
        'context': context
    })


def booking(request):
    if request == 'GET':
        return render(request, 'login/index.html')
    else:
        terminal = request.POST.get('terminal', None)
        departuretime = request.POST.get('departuretime', None)

    return render(request, 'booking/booking.html')