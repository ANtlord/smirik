from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required
from .views import UserCreationView
from .views import UserDetailView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^registration/$', UserCreationView.as_view(),
        name='registration_url'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name':
        'smirik_auth/authorization.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'},
        name='logout'),
    url(r'^account/$', login_required(UserDetailView.as_view()),
        name='account_view'),
)
