from django.conf.urls import patterns, url
from .views import HomepageView
from .views import PageView

urlpatterns = patterns('',
    url(r'^$', HomepageView.as_view(), name='homepage', kwargs={'slug': 'home'}),
    url(r'^(?P<path>.*)/$', PageView.as_view(), name='page'),
)
