from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Entry(models.Model):
	title = models.CharField(max_length=100)
	category = models.CharField(max_length=100)
	subcategory = models.CharField(max_length=100, default=None)
	description = models.TextField()
	add_date = models.DateTimeField('date added')

	def __str__(self):
		return self.title

	class Meta:
		ordering = ('title',)
		# db_table = 'Entries'


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	entries = models.ManyToManyField(Entry)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ('name',)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Tip(models.Model):
	author = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
	topic = models.ForeignKey(Entry, models.PROTECT)
	body = models.TextField()
	votes = models.IntegerField(default=0)
	add_date = models.DateTimeField('date added')

	def __str__(self):
		return self.topic, self.author, self.body

	class Meta:
		ordering = ('topic',)