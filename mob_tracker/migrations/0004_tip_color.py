# Generated by Django 2.0.3 on 2018-06-07 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mob_tracker', '0003_auto_20180607_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='tip',
            name='color',
            field=models.CharField(default='#ffffff', max_length=7),
        ),
    ]
