from django.db import models

class UserInfo(models.Model):
    '''
    用户表
    '''
    name = models.CharField(verbose_name="姓名",max_length=32)
    pwd = models.CharField(verbose_name="密码",max_length=64)

    def __str__(self):
        return self.name


class Room(models.Model):
    '''
    会议室
    '''
    title = models.CharField(verbose_name="会议室名字",max_length=32)
    def __str__(self):
        return self.title

class Select(models.Model):
    '''
    记录表
    '''
    user = models.ForeignKey(to=UserInfo)
    room = models.ForeignKey(to=Room)

    time_choices=(
        (1,"8:00"),
        (2,"9:00"),
        (3,"10:00"),
        (4,"11:00"),
        (5,"12:00"),
        (6,"13:00"),
        (7,"14:00"),
        (8,"15:00"),
        (9,"16:00"),
        (10,"17:00"),
        (11,"18:00"),
        (12,"19:00"),
        (13,"20:00"),
    )
    time = models.IntegerField(verbose_name="时间段",choices=time_choices)
    data = models.DateField(verbose_name="日期")

    class Meta:
        unique_together = ('room','time','data')
    def __str__(self):
        return  self.user.name
