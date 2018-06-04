from django import forms
from .models import Entry, Tip

# class CatForm(forms.ModelForm):
# 	class Meta:
# 		model = Cat
# 		fields = ['name', 'breed', 'description', 'age']

class LoginForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=64)
    password = forms.CharField(label="Password", widget=forms.PasswordInput())