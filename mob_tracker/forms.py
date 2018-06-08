from django import forms
from .models import Entry, Tip
from django.contrib.auth.models import User


class LoginForm(forms.Form):
	username = forms.CharField(label="Username", max_length=64)
	password = forms.CharField(label="Password", widget=forms.PasswordInput())

class UserForm(forms.Form):
	username = forms.CharField(label="Username", max_length=64)
	email = forms.CharField(label="Email", max_length=128, widget=forms.EmailInput())
	password = forms.CharField(label="Password", max_length=64, widget=forms.PasswordInput())

class SearchForm(forms.Form):
	query = forms.CharField(max_length=200)

class EntryForm(forms.Form):
	title = forms.CharField(max_length=100)
	category = forms.CharField(max_length=100)
	subcategory = forms.CharField(max_length=100, required=False)
	description = forms.CharField(max_length=200, required=False)

class TipForm(forms.Form):
	# author = forms.IntegerField()
	# topic = forms.IntegerField()
	body = forms.CharField(max_length=200)
	# votes = forms.IntegerField()
	# voters = models.ManyToManyField('Profile', through=Profile, blank=True, default=None)
	# add_date = models.DateTimeField('date added', default=datetime.now, blank=True)

# class TipVoteForm(forms.Form):
# 	tip = forms.IntegerField()
# 	user = forms.IntegerField()
# 	polarity = forms.BooleanField()