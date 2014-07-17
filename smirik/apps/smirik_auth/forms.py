# -*- coding: utf-8 -*-
from django.contrib.auth import forms as base
from django.contrib.auth import get_user_model
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

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name')

class UserChangeForm(base.UserChangeForm):
    class Meta:
        model = get_user_model()
