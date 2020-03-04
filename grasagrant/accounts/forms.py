from django import forms
from .models import User
from django.contrib.auth.admin import UserAdmin as auth_UserAdmin
from django.contrib.auth.forms import UserChangeForm as auth_UserChangeForm
from django.contrib.auth.forms import UserCreationForm as auth_UserCreationForm


class SignupForm(auth_UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email')



class UserChangeForm(auth_UserChangeForm):
    class Meta(auth_UserChangeForm.Meta):
        model = User
        fields = ('username', 'email')

class UserCreationForm(auth_UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'email')
