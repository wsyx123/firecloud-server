# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-12-27 01:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_ansiblehost_ansiblelog'),
    ]

    operations = [
        migrations.AddField(
            model_name='ansiblelog',
            name='total_task_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
