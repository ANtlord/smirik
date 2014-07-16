# -*- coding: utf-8 -*-
from django.contrib.auth import forms as base
from django.contrib.auth import get_user_model
User = get_user_model()

class UserCreationForm(base.UserCreationForm):
    error_css_class = 'registration_error'
    auth_error = None
    password = None

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name')

class UserChangeForm(base.UserChangeForm):
    class Meta:
        model = get_user_model()
