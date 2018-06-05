from django import forms
from .models import Entry, Tip
from django.contrib.auth.models import User

# class CatForm(forms.ModelForm):
# 	class Meta:
# 		model = Cat
# 		fields = ['name', 'breed', 'description', 'age']

class LoginForm(forms.Form):
	username = forms.CharField(label="Username", max_length=64)
	password = forms.CharField(label="Password", widget=forms.PasswordInput())

class UserForm(forms.Form):
	first_name = forms.CharField(label="First Name", max_length=64)
	last_name = forms.CharField(label="Last Name", max_length=128)
	username = forms.CharField(label="Username", max_length=64)
	email = forms.CharField(label="Email", max_length=128, widget=forms.EmailInput())
	password = forms.CharField(label="Password", max_length=64, widget=forms.PasswordInput())

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'username', 'email', 'password')

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('name')
