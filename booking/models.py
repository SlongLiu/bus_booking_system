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

    usertype = ('user', 'busdriver', 'employee')

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class Line(models.Madel):
    '''
    线路信息
    '''

    name = models.CharField(max_length=256, unique=True)
    destination = models.CharField(max_length=256)
    service_time_start = models.TimeField()
    service_time_end = models.TimeField()

    def __str__(self):
        return self.name


class PriceOfLine(models.Model):
    '''
    票价信息
    '''

    line = models.ForeignKey(to='Line', to_field='name')
    site = models.CharField(max_length=256)
    price = models.FloatField()


class Shuttle(models.Model):
    '''
    大巴信息
    '''

    line = models.ForeignKey(to='Line', to_field='name')
    plate = models.CharField(max_length=64, unique=True)


class Departure(models.Model):
    '''
    车的班次信息
    '''

    shuttle_id = models.ForeignKey(to='Shuttle', to_field='id')
    datetime = models.DateTimeField()
    busdriver_id = models.ForeignKey(to='User', to_field='id')

