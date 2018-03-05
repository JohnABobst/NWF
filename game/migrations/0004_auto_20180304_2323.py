# Generated by Django 2.0.2 on 2018-03-05 07:23

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0003_auto_20180304_1854'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='magic_card',
            name='player',
        ),
        migrations.RemoveField(
            model_name='ingame',
            name='submissions',
        ),
        migrations.AlterUniqueTogether(
            name='ingame',
            unique_together={('game', 'player')},
        ),
        migrations.DeleteModel(
            name='magic_card',
        ),
    ]
