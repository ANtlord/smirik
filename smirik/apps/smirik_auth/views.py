# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import get_object_or_404
from django.shortcuts import Http404
from django.views.generic import CreateView
from django.views.generic import DetailView
from .forms import UserCreationForm
from django.conf import settings
from smirik.apps.financeapp.forms import StockForm

class UserViewMixin(object):
    user_id = None

    def get(self, request, *args, **kwargs):
        self.user_id = request.user.id
        return super(UserViewMixin, self).get(request, *args, **kwargs)


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


class UserDetailView(UserViewMixin, DetailView):
    """Class for represent user's account"""
    model = get_user_model()
    template_name = 'smirik_auth/account.html'

    def get_object(self):
        """
        Method for get instance of model "User"
        """
        return get_object_or_404(self.model, pk=self.user_id)

    def get_context_data(self, **kwargs):
        ctx = super(UserDetailView, self).get_context_data(**kwargs)
        ctx['form'] = StockForm()
        return ctx
