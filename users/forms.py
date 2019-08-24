from captcha.fields import ReCaptchaField

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from captcha.fields import ReCaptchaField


class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserRegisterForm(forms.ModelForm):
	
	class Meta():
		model=Profile
		fields=('image',)




class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ['username', 'email',]

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model=Profile
		fields=('image',)