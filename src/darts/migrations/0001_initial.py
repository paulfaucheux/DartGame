# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-12-13 11:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DartName', models.CharField(max_length=100)),
                ('TotalValue', models.IntegerField()),
                ('TimeValue', models.IntegerField()),
                ('ValueDart', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CreatedDate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='LnkDartPlayedScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LnkGamePlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Order', models.IntegerField()),
                ('Game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='darts.Game')),
            ],
        ),
        migrations.CreateModel(
            name='LnkGamePlayerDartPlayed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Turn', models.IntegerField()),
                ('Dart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='darts.Dart')),
                ('LnkGamePlayer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='darts.LnkGamePlayer')),
            ],
        ),
        migrations.CreateModel(
            name='LnkGamePlayerScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ScoreValue', models.IntegerField()),
                ('DisplayOrder', models.IntegerField()),
                ('ScoreName', models.CharField(max_length=6)),
                ('LnkGamePlayer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='darts.LnkGamePlayer')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PlayerName', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='RefGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GameName', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='lnkgameplayer',
            name='Player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='darts.Player'),
        ),
        migrations.AddField(
            model_name='lnkdartplayedscore',
            name='DartPlayed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='darts.LnkGamePlayerDartPlayed'),
        ),
        migrations.AddField(
            model_name='lnkdartplayedscore',
            name='PlayerScore',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='darts.LnkGamePlayerScore'),
        ),
        migrations.AddField(
            model_name='game',
            name='GameName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='darts.RefGame'),
        ),
    ]
