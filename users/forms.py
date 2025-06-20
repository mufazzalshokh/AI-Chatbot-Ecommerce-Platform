from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import ProfileModel


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        exclude = ['user']


class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
