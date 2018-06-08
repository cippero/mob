# Generated by Django 2.0.3 on 2018-06-07 19:08

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mob_tracker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipVotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polarity', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='tips',
            field=models.ManyToManyField(blank=True, default=None, to='mob_tracker.Tip'),
        ),
        migrations.AddField(
            model_name='tip',
            name='voters',
            field=models.ManyToManyField(blank=True, default=None, to='mob_tracker.Profile'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='add_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='date added'),
        ),
        migrations.AlterField(
            model_name='tip',
            name='add_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='date added'),
        ),
        migrations.AddField(
            model_name='tipvotes',
            name='tip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mob_tracker.Tip'),
        ),
        migrations.AddField(
            model_name='tipvotes',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
