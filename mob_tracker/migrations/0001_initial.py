# Generated by Django 2.0.3 on 2018-06-05 22:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_clean', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('subcategory', models.CharField(default=None, max_length=100)),
                ('description', models.TextField(default=None)),
                ('add_date', models.DateTimeField(verbose_name='date added')),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entries', models.ManyToManyField(blank=True, to='mob_tracker.Entry')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('votes', models.IntegerField(default=0)),
                ('add_date', models.DateTimeField(verbose_name='date added')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mob_tracker.Entry')),
            ],
            options={
                'ordering': ('topic',),
            },
        ),
        migrations.AddField(
            model_name='entry',
            name='contributors',
            field=models.ManyToManyField(blank=True, to='mob_tracker.Profile'),
        ),
    ]
