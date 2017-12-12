# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-11 06:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='会议室名字')),
            ],
        ),
        migrations.CreateModel(
            name='Select',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField(choices=[(1, '8:00'), (2, '9:00'), (3, '10:00'), (4, '11:00'), (5, '12:00'), (6, '13:00'), (7, '14:00'), (8, '15:00'), (9, '16:00'), (10, '17:00'), (11, '18:00'), (12, '19:00'), (13, '20:00')], verbose_name='时间段')),
                ('data', models.DateField(verbose_name='日期')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app0.Room')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('pwd', models.CharField(max_length=64, verbose_name='密码')),
            ],
        ),
        migrations.AddField(
            model_name='select',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app0.UserInfo'),
        ),
        migrations.AlterUniqueTogether(
            name='select',
            unique_together=set([('room', 'time', 'data')]),
        ),
    ]
