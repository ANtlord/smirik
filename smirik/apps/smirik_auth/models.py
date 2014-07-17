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

class Item(models.Model):
    """Item of user's portfolio"""
    class Meta:
        verbose_name = u'Элемент портфолио'
        verbose_name_plural = u'Элементы портфолио'

    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='items')

    def __unicode__(self):
        return self.name

    #@models.permalink
    #def get_absolute_url(self):
        #return ('view_or_url_name' pk)
