# Generated by Django 2.0.3 on 2018-06-07 19:20

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mob_tracker', '0002_auto_20180607_1208'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TipVotes',
            new_name='TipVote',
        ),
        migrations.AlterModelOptions(
            name='tipvote',
            options={'ordering': ('tip',)},
        ),
    ]