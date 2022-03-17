from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile, RestaurantAdmin


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["avatar", "name", "phone"]


class RestaurantAdminAdd(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class RestaurantAdminForm(forms.ModelForm):
    class Meta:
        model = RestaurantAdmin
        fields = [
            "avatar",
            "name",
            "phone",
            "role",
            "is_active",
        ]


class RestaurantAdminLoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
