# Generated by Django 4.0 on 2022-01-13 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chess', '0004_alter_game_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='winner',
        ),
        migrations.AddField(
            model_name='game',
            name='result',
            field=models.IntegerField(blank=True, choices=[(1, 'Game created'), (2, 'Game in progress'), (3, 'Game completed')], default=1, null=True),
        ),
    ]
