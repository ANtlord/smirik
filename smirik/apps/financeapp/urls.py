from django.conf.urls import patterns, url
from .views import StockListView
from .views import StockCreateView
from .views import StockDeleteView
from .views import StockDetailView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns('',
    url(r'^stock-list/$', login_required(StockListView.as_view()),
        name='stock_list'),
    url(r'^stock-create/$', login_required(StockCreateView.as_view()),
        name='stock_create'),
    url(r'^stock-delete/(?P<pk>[^/]*)/$', csrf_exempt(StockDeleteView.as_view()),
        name='stock_delete'),
    url(r'^stock-detail/(?P<pk>[^/]*)/$', login_required(StockDetailView.as_view()),
        name='stock_detail'),
)
