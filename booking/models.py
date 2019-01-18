from django.db import models
from django.utils import timezone
# Create your models here.


class Message(models.Model):
    '''
    用户消息
    '''
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class User(models.Model):
    '''
    用户信息
    '''

    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    usertype = (
        ('user', '用户'),
        ('busdriver', '大巴司机'),
        ('employee', '公司员工')
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    c_time = models.DateTimeField(auto_now_add=True)
    identify = models.CharField(max_length=32, choices=usertype, default='用户')
    mobile = models.CharField(max_length=32, unique=True)
    realname = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class Line(models.Model):
    '''
    线路信息
    '''

    name = models.CharField(max_length=128, unique=True)
    destination = models.CharField(max_length=128)
    service_time_start = models.TimeField()
    service_time_end = models.TimeField()

    def __str__(self):
        return self.name


class PriceOfLine(models.Model):
    '''
    票价信息
    '''

    line = models.ForeignKey(to='Line', to_field='name', on_delete=models.CASCADE)
    site = models.CharField(max_length=128)
    price = models.FloatField()


class Shuttle(models.Model):
    '''
    大巴信息
    '''

    line = models.ForeignKey(to='Line', to_field='name', on_delete=models.CASCADE)
    plate = models.CharField(max_length=64, unique=True)


class Departure(models.Model):
    '''
    车的班次信息
    '''

    shuttle_id = models.ForeignKey(to='Shuttle', to_field='id', on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    busdriver_id = models.ForeignKey(to='User', to_field='id', on_delete=models.CASCADE)

