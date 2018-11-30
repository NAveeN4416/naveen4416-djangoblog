from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
	first_name  = forms.CharField(max_length='30',required=True,help_text='20 Chars')
	last_name   = forms.CharField(max_length='30',required=True,help_text='20 Chars')
	email	    = forms.EmailField(max_length='30',required=True,help_text='eg : example@gmail.com')
	register_as	= forms.IntegerField(required=True,help_text='Select')


	class Meta:
		model  = User
		fields = ('username','first_name','last_name','email','password1','password2')


