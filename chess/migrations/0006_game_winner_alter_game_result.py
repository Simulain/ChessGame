# Generated by Django 4.0 on 2022-01-16 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('chess', '0005_remove_game_winner_game_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner', to='auth.user'),
        ),
        migrations.AlterField(
            model_name='game',
            name='result',
            field=models.IntegerField(blank=True, choices=[(1, 'Winner: white'), (2, 'Winner: black'), (3, 'Draw')], default=1, null=True),
        ),
    ]