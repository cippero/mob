# Generated by Django 2.0.3 on 2018-06-08 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mob_tracker', '0005_auto_20180607_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='description',
            field=models.TextField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='entry',
            name='subcategory',
            field=models.CharField(blank=True, default=None, max_length=100),
        ),
    ]