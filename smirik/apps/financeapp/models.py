from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
User = get_user_model()


class Stock(models.Model):
    """Item of user's portfolio"""
    class Meta:
        verbose_name = u'Элемент портфолио'
        verbose_name_plural = u'Элементы портфолио'

    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='items')
    count = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(default=timezone.now)

    def clean(self):
        if len(Stock.objects.filter(name=self.name, user_id=self.user_id)):
            raise ValidationError(u'Сток с таким именем уже существует')
        else: super(Stock, self).clean()

    def __unicode__(self):
        return self.name

    #@models.permalink
    #def get_absolute_url(self):
        #return ('view_or_url_name' pk)

# Create your models here.
