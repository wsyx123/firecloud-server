# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-12-31 07:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20181231_0529'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileModelExistList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=32)),
                ('file_path', models.CharField(max_length=64)),
                ('file_size', models.CharField(max_length=8)),
                ('task_name', models.CharField(max_length=32)),
            ],
        ),
        migrations.RemoveField(
            model_name='filemodelforhad',
            name='file_path',
        ),
        migrations.RemoveField(
            model_name='filemodelforhad',
            name='file_size',
        ),
        migrations.AlterField(
            model_name='filemodelforhad',
            name='file_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.FileModelExistList'),
        ),
        migrations.AlterField(
            model_name='filemodelforurl',
            name='url',
            field=models.CharField(max_length=128),
        ),
    ]
