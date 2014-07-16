# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import get_object_or_404
from django.shortcuts import Http404
from django.views.generic import CreateView
from django.views.generic import TemplateView
from .forms import UserCreationForm
from django.conf import settings

class UserFormViewMixin(object):
    def get_form_kwargs(self):
        kwargs = super(UserFormViewMixin, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.id
        return kwargs

class UserCreationView(CreateView):
    template_name = 'smirik_auth/registration.html'
    form_class = UserCreationForm

    def get_success_url(self):
        return '/complete-registration/'
