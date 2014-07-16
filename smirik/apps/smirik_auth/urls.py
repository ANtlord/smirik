from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required
from .views import UserCreationView

urlpatterns = patterns('',
    url(r'^registration/$', UserCreationView.as_view(),
        name='registration_url'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name':
        'smirik_auth/authorization.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'},
        name='logout'),
)
