from django.shortcuts import Http404
from django.shortcuts import HttpResponse
from smirik.apps.smirik_auth.views import UserFormViewMixin
from smirik.apps.smirik_auth.views import UserViewMixin
from django.views.generic import CreateView
from django.views.generic import ListView
from .forms import StockForm
from .models import Stock
from django.core import serializers
import urllib.request
import urllib.parse
import json

class StockCreateView(CreateView, UserFormViewMixin):
    """Class for creation stock"""
    form_class = StockForm

    def get(self, request, *args, **kwargs):
        raise Http404


class StockListView(UserViewMixin, ListView):
    """ Class for represent stock of current user. """
    model = Stock
    def get(self, request, *args, **kwargs):
        super(StockListView, self).get(request, *args, **kwargs)
        symbols = []
        for item in self.object_list:
            symbols.append(item.name)

        symbols_str = '", "'.join(symbols)
        symbols_str = '("%s")' % symbols_str

        fields = ', '.join(['Ask', 'Change', 'Bid', 'Open', 'DaysHigh', 'DaysLow'])

        QUERY = "select %s from yahoo.finance.quotes where symbol in %s" % (fields, symbols_str)
        base_url = "https://query.yahooapis.com/v1/public/yql?q=%s" % urllib.parse.quote(QUERY)
        url = base_url+'&format=json&diagnostics=true&env=http%3A%2F%2Fdatatables.org%2Falltables.env&callback='
        res = urllib.request.urlopen(url)
        json_res = res.read()
        stocks = json.loads(json_res.decode('utf-8'))

        result_array = []
        if type(stocks['query']['results']['quote']) == dict:
            stocks['query']['results']['quote'].update({
                'Symbol' : self.object_list[0].name
            })
            result_array.append(stocks['query']['results']['quote'])
        else:
            i=0
            for item in stocks['query']['results']['quote']:
                item['Symbol'] = self.object_list[i].name
                i+=1
                result_array.append(item)

        return HttpResponse(json.dumps(result_array),
                'application/json; charset=UTF-8')
    

    def get_queryset(self, **kwargs):
        qs = super(StockListView, self).get_queryset(**kwargs)
        qs = qs.filter(user_id=self.user_id)
        return qs
