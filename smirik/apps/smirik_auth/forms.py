# -*- coding: utf-8 -*-
from django.contrib.auth import forms as base
from django.contrib.auth import get_user_model
from django import forms
User = get_user_model()

class UserFormMixin(object):
    """Mixin for forms, which depend of user."""
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)
        super(UserFormMixin, self).__init__(*args, **kwargs)
        if user_id: self.instance.user_id = user_id

class UserCreationForm(base.UserCreationForm):
    error_css_class = 'registration_error'
    auth_error = None
    password = None

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

class UserChangeForm(base.UserChangeForm):
    class Meta:
        model = User
