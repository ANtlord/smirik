from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Stock(models.Model):
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

# Create your models here.
