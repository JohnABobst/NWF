# Generated by Django 2.0.4 on 2018-04-22 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0017_auto_20180419_1053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='magic_card',
            name='card_sub_types',
        ),
        migrations.AlterField(
            model_name='magic_card',
            name='card_type',
            field=models.CharField(max_length=256),
        ),
    ]