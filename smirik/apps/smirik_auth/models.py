# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'
    
    def __unicode__(self):
        return self.username

    @models.permalink
    def get_absolute_url(self):
        return ('profile_view', (), {'pk': self.pk})
