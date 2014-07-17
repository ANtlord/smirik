# -*- coding: utf-8 -*-
from django.db import models
from ckeditor.fields import RichTextField


class Page(models.Model):
    class Meta:
        verbose_name=u'Страница'
        verbose_name_plural=u'Страницы'

    name = models.CharField(max_length=255, verbose_name=u'Название')
    slug = models.SlugField(max_length=255, unique=True,
            help_text=u'Для главной страницы значение должно быть "home"')
    text = RichTextField(max_length=5000, verbose_name=u'Текст')
    path = models.CharField(max_length=300, verbose_name=u'Полный путь',
            null=True, blank=True, help_text=u'Генерируется автоматически')

    def save(self, *args, **kwargs):
        if not 'force_insert' in kwargs:
            kwargs['force_insert'] = False
        if not 'force_update' in kwargs:
            kwargs['force_update'] = False

        if self.slug == 'home':
            self.path = '/'
        else:
            self.path = '/'+self.slug+'/'
        super(Page, self).save()

    def get_absolute_url(self):
        return self.path
