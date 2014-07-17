from django.conf.urls import patterns, url
from .views import StockListView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^stock-list/$', login_required(StockListView.as_view()),
        name='stock_list'),
)
