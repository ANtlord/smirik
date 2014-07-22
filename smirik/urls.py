from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'smirik.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^', include('smirik.apps.smirik_auth.urls')),
    url(r'^', include('smirik.apps.financeapp.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^', include('smirik.apps.pages.urls')),
)
