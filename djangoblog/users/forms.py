from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class Registration(UserCreationForm):
	first_name  = forms.CharField(max_length='30',required=True,help_text='20 Chars')
	last_name   = forms.CharField(max_length='30',required=True,help_text='20 Chars')
	email	    = forms.EmailField(max_length='30',required=True,help_text='eg : example@gmail.com')


	class Meta:
		model  = User
		fields = ('username','first_name','last_name','email','password1','password2')


