# Generated by Django 2.0.4 on 2018-04-19 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0016_auto_20180419_0518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magic_card',
            name='card_color',
            field=models.CharField(choices=[('Blue', 'Blue'), ('Red', 'Red'), ('White', 'White'), ('Black', 'Black'), ('Green', 'Green'), ('Colorless', 'Colorless')], max_length=15),
        ),
    ]