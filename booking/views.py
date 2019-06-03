from django.http import HttpResponseRedirect
# Create your views here.
from django.http import HttpResponse
from booking import models
from django.shortcuts import render, redirect
from .forms import UserForm, RegisterForm
import hashlib
from django.forms.models import model_to_dict
import datetime
import re


def hash_code(s, salt='ojbk'):
    h = hashlib.sha3_256()
    s += salt
    h.update(s.encode())
    # print('h=', h.hexdigest())
    return h.hexdigest()


def first_request(request):
    return HttpResponse('Hello world!')


def index(request):
    # pass
    return render(request, 'index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

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
                    if user.identify == 'employee':
                        return redirect('/manage_orders/')
                    elif user.identify == 'user':
                        return redirect('/browse/')
                    elif user.identify == 'busdriver':
                        return redirect('/validation/')
                    else:
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
            # print(i)
            i = datetime.time((i.hour+interval.hour + (i.minute+interval.minute) // 60) % 24, \
                              (i.minute+interval.minute) % 60, 0)
        # print(timetable)
        item_dict['timetable'] = timetable
        context.append(item_dict)

    return render(request, 'booking/browse.html', {
        'num': len(context),
        'context': context
    })


def seat_coding(x):
    x1 = x // 4
    if x % 4 != 0:
        x1 = x1 + 1
    x2 = x % 4
    if x2 == 1:
        x2 = 3
    elif x2 == 2:
        x2 = 4
    elif x2 == 3:
        x2 = 6
    else:
        x2 = 7
    return(str(x1) + '排' + str(x2) + '座')


def booking(request):
    if request.method == 'GET':
        return render(request, 'login/index.html')
    else:
        terminal = request.POST.get('terminal', None).split(':')[0]
        price = request.POST.get('terminal', None).split(':')[1]
        departuretime = request.POST.get('departuretime', None)
        departuredate = request.POST.get('departuredate', '2019-02-01')
        name = request.POST.get('name', None)

        print('name=', name)
        print('departuredate=', departuredate)
        print('departuretime=', departuretime)
        print('terminal=', terminal)
        print('price=', price)

        # 查询有没有合适的车 departure表里
        line_id = models.Line.objects.get(name=name).id
        # print('line_id=', line_id)

        shuttle_id = list(models.Shuttle.objects.filter(line_id=line_id).values('id'))
        # print('shuttle_id=', shuttle_id)

        departuretime_list = departuretime.split(':')
        if len(departuretime_list)<3:
            departuretime_list.append('0')
        departuredate_list = departuredate.split('-')
        pretime = datetime.datetime(int(departuredate_list[0]), int(departuredate_list[1]), int(departuredate_list[2]), \
                  (int(departuretime_list[0])+8+24) % 24, int(departuretime_list[1]), int(departuretime_list[2]))
        # print('pretime=', pretime)
        shuttle_id_in_time = models.Departure.objects.filter(datetime=pretime)
        # print('shuttle_id_in_time=', shuttle_id_in_time)

        # 把合适的车做成一个集合
        candidate = set()
        for one in shuttle_id:
            # print('one[id]=', one['id'])
            candidate.add(one['id'])
        # print('candidate=', candidate)
        # 查看有没有合适的排班
        avi = -1
        departure_id = -1
        for one in shuttle_id_in_time:
            if one.shuttle_id in candidate:
                # 查询这个车还有没有座
                orders = models.Order.objects.filter(departure_id=one.shuttle_id)
                if len(orders) >= 40:
                    continue
                else:
                    avi = one.shuttle_id
                    departure_id = one.id
                    unavi_seat = []
                    for u in orders:
                        unavi_seat.append(u.seat)
                    break

    # print('avi=', avi)
    if avi == -1:
        return render(request, 'booking/no-result.html')
        # test = models.Departure.objects.get(id=1)
        # print('test=', test.datetime)
    # print('avi=', avi)

    unavi_seat_gen = []
    for x in unavi_seat:
        x1 = x // 4
        if x % 4 != 0:
            x1 = x1 + 1
        x2 = x % 4
        if x2 == 1:
            x2 = 3
        elif x2 == 2:
            x2 = 4
        elif x2 == 3:
            x2 = 6
        else:
            x2 =7
        unavi_seat_gen.append(str(x1)+'_'+str(x2))
    print('unavi_seat_gen=',unavi_seat_gen)

    return render(request, 'booking/booking.html', {
        'name': name,
        'terminal': terminal,
        'price': price,
        'departuredate': departuredate,
        'departuretime': departuretime,
        'unavi_seat': unavi_seat_gen, # ['2_3', '3_4', '6_7']测试可用
        'departure_id': departure_id
    })


def no_result(request):
    return render(request, 'booking/no-result.html')


def result(request):
    if request.method == 'GET':
        return render(request, 'login/index.html')
    else:
        seat = request.POST.get('seat', None)
        departure_id = request.POST.get('departure_id', None)
        user_id = request.session['user_id']
        # cart = request.session['cart']
        print('seat=', seat)
        print('departure_id=', departure_id)
        print('user_id=', user_id)
        # print('cart=', cart)

        seat_num = re.findall(r'\d+', seat)
        print(seat_num)
        x2 = -1
        if seat_num[1] == '3':
            x2 = 1
        elif seat_num[1] == '4':
            x2 = 2
        elif seat_num[1] == '6':
            x2 = 3
        else:
            x2 = 4
        seat_count = (int(seat_num[0])-1)*4+x2
        print('seat_count=', seat_count)

        # 添加到数据库中
        getuser = models.User.objects.get(id=user_id)
        getdeparture = models.Departure.objects.get(id=departure_id)
        newOrder = {
            'user': getuser,
            'seat': seat_count,
            'departure': getdeparture
        }
        new_order = models.Order.objects.create(**newOrder)
        # new_order.user = user_id
        # new_order.seat = seat_count
        # new_order.departure = departure_id
        new_order.save()

    return render(request, 'booking/result.html')


def validation(request):
    message = ''
    if request.method == 'POST':
        order_id = request.POST.get('order_id', None)
        print('order_id=', order_id)
        obj = models.Order.objects.get(id=order_id)
        obj.validation = 'y'
        obj.save()
        print(order_id,'检票成功')
        message = '检票成功'


    print(request.session['identify'])

    departure = models.Departure.objects.filter(busdriver_id=request.session['user_id'])
    departure_list = []
    for x in departure:
        orders_model = models.Order.objects.filter(id=x.id)
        orders = []
        for order in orders_model:
            w = {
                'user_id': order.user_id,
                'seat': seat_coding(order.seat),
                'order_id': order.id,
                'validation': order.validation
            }
            orders.append(w)
        dep = {
            'id': x.id,
            'datetime': x.datetime,
            'shuttle': x.shuttle_id,
            'orders': orders,
            'num': len(orders)
        }
        print(dep)
        departure_list.append(dep)

    return render(request, 'manage/validation.html', {
        'departure': departure_list,
        'message': message
    })


def manage(request):
    print('request.method=', request.method)
    userinfo = models.User.objects.filter(identify='user')
    print('userinfo=', userinfo)
    userinfo_list = []
    for user in userinfo:
        one = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'sex': user.sex,
            'mobile': user.mobile,
            'realname': user.realname
        }
        userinfo_list.append(one)

    return render(request, 'manage/management.html', {
        'usernum': len(userinfo_list),
        'users': userinfo_list
    })


def manage_orders(request):
    print('request.method=', request.method)
    orderinfo = models.Order.objects.all()
    print('orderinfo=', orderinfo)
    orderinfo_list = []
    for order in orderinfo:
        # print(order.user.)
        # username = list(models.User.objects.filter(id=int(order.user)))[0].name
        # adeparture = list(models.Departure.objects.filter(id=order.departure))[0]
        # datetime = adeparture.datetime
        # busdriver_id = adeparture.busdriver_id
        # busdriver_name = list(models.User.objects.filter(id=busdriver_id))[0].name
        # shuttle_id = adeparture.shuttle_id
        # shuttle = list(models.Shuttle.objects.filter(id=shuttle_id))[0]
        # shuttle_line = shuttle.line
        # shuttle_plate = shuttle.shuttle_plate

        one = {
            'id': order.id,
            'user': order.user,
            'username': order.user.name,

            'departure_id': order.departure,
            'datetime': order.departure.datetime,
            'busdriver_id': order.departure.busdriver,
            'busdriver_name': order.departure.busdriver.name,

            'shuttle_id': order.departure.shuttle,
            'shuttle_line': order.departure.shuttle.line,
            'shuttle_plate': order.departure.shuttle.plate,

            'seat': order.seat,
            'validation': order.validation
        }

        orderinfo_list.append(one)
        print(one)
    return render(request, 'manage/manage_orders.html', {
        'ordernum': len(orderinfo_list),
        'orders': orderinfo_list
    })


def del_order(request, id):
    if request.session['identify'] != 'employee':
        return redirect('/index/')
    del_obj = models.Order.objects.get(id=id)
    del_obj.delete()

    return redirect('/manage_orders/')
