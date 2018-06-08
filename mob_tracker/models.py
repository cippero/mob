from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

class Entry(models.Model):
	title_clean = models.CharField(max_length=100, unique=True)
	title = models.CharField(max_length=100)
	category = models.CharField(max_length=100)
	subcategory = models.CharField(max_length=100, default=None, blank=True)
	description = models.TextField(default=None, blank=True)
	add_date = models.DateTimeField('date added', default=datetime.now, blank=True)
	contributors = models.ManyToManyField('Profile', blank=True)

	def __str__(self):
		return self.title_clean

	class Meta:
		ordering = ('title',)


class Tip(models.Model):
	author = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
	topic = models.ForeignKey(Entry, models.PROTECT)
	body = models.TextField()
	votes = models.IntegerField(default=0)
	voters = models.ManyToManyField('Profile', blank=True, default=None)
	add_date = models.DateTimeField('date added', default=datetime.now, blank=True)
	color = models.CharField(max_length=11, default='255,255,255')

	# def __str__(self):
		# return '%s, %s, %s' % (self.topic, self.author, self.body)
		# return self.topic

	class Meta:
		ordering = ('topic',)

class TipVote(models.Model):
	tip = models.ForeignKey(Tip, on_delete=models.CASCADE)
	user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
	polarity = models.BooleanField()

	# def __str__(self):
	# 	return self.tip

	class Meta:
		ordering = ('tip',)


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	entries = models.ManyToManyField('Entry', through=Entry.contributors.through, blank=True)
	tips = models.ManyToManyField('Tip', through=Tip.voters.through, blank=True, default=None)

	def __str__(self):
		return self.user.username

	# class Meta:
	# 	ordering = ('username',)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()