# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-02-05 17:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('darts', '0002_auto_20180204_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='lnkgameplayerdartplayed',
            name='TurnDart',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
