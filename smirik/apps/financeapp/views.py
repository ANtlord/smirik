from django.shortcuts import Http404
from django.shortcuts import HttpResponse
from smirik.apps.smirik_auth.views import UserFormViewMixin
from smirik.apps.smirik_auth.views import UserViewMixin
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from .forms import StockForm
from .models import Stock
from django.core import serializers
import urllib.request
import urllib.parse
import json
import datetime

STOCK_FIELDS = ['Ask', 'Change', 'Open', 'DaysHigh', 'DaysLow']

class JsonFormViewMixin(object):
    def form_valid(self, form):
        res = super(JsonFormViewMixin, self).form_valid(form)
        return HttpResponse('OK')

    def form_invalid(self, form):
        res = super(JsonFormViewMixin, self).form_invalid(form)
        return HttpResponse(json.dumps(form._errors),
                'application/json; charset=UTF-8')


class StockCreateView(UserFormViewMixin, JsonFormViewMixin, CreateView):
    """Class for creation stock"""
    form_class = StockForm
    template_name = 'empty.html'

    def get_success_url(self):
        return '/account/'


class StockDeleteView(DeleteView, JsonFormViewMixin):
    model = Stock
        
    def get_success_url(self):
        return '/account/'


class APIMixin(object):
    BASE_URL = "https://query.yahooapis.com/v1/public/yql?q=" 
    ADDITIONAL_PARAMS = ('&format=json&diagnostics=true&'
            +'env=http%3A%2F%2Fdatatables.org%2Falltables.env&callback=')

    def get_url(self, query):
        """Method returns base of url for request to YAHOO Finance

        :query: @ is string of YQL query
        :returns: @ prepared url for reuqest.

        """
        return self.BASE_URL+urllib.parse.quote(query)+self.ADDITIONAL_PARAMS

    def parse_response_for_object(self, response):
        result_array = []
        response_dict = json.loads(response.decode('utf-8'))
        if type(response_dict['query']['results']['quote']) == dict:
            result_array.append(response_dict['query']['results']['quote'])
        # Parsing list of objects.
        else:
            i=0
            for item in response_dict['query']['results']['quote']:
                i+=1
                result_array.append(item)
        return result_array


    def parse_response_for_object_list(self, json_res):
        """Method parses response from YAHOO

        :json_res: @byte array, must be json valid.
        :returns: @array of object, which have been parsed from resonse.
        """
        result_array = []
        response_dict = json.loads(json_res.decode('utf-8'))
        if type(response_dict['query']['results']['quote']) == dict:
            item = response_dict['query']['results']['quote']
            item.update({
                'Symbol' : self.object_list[0].name,
                'pk' : self.object_list[0].pk,
                'count': self.object_list[0].count
            })
            result_array.append(item)
        # Parsing list of objects.
        else:
            i=0
            for item in response_dict['query']['results']['quote']:
                item['Symbol'] = self.object_list[i].name
                item['pk'] = self.object_list[i].pk
                item['count'] = self.object_list[i].count
                i+=1
                result_array.append(item)
        return result_array

        # It means, that current class represent list.
        #if hasattr(self, 'object_list') and self.object_list:
            #return self.__parse_response(response_obj)
        ## It means, that current class represent single instance.
        #elif not hasattr(self, 'object_list'):
            #return self.__parse_response(response_obj)
        ## It means, that somethins it's wrong.
        #else: return None


class StockListView(UserViewMixin, ListView, APIMixin):
    """ Class for represent stock of current user. """
    model = Stock
    def get(self, request, *args, **kwargs):
        super(StockListView, self).get(request, *args, **kwargs)
        symbols = []    # symbols of stocks.
        if len(self.object_list) != 0:
            for item in self.object_list:
                symbols.append(item.name)

            # Serializing for sending to request.
            symbols_str = '", "'.join(symbols)
            symbols_str = '("%s")' % symbols_str

            fields = ', '.join(STOCK_FIELDS)

            # Build query string and receive response.
            QUERY = "select %s from yahoo.finance.quotes where symbol in %s" % (fields, symbols_str)
            res = urllib.request.urlopen(self.get_url(QUERY))
            json_res = res.read()

            # Parse incoming data for frontend.
            result_array = self.parse_response_for_object_list(json_res)
            return HttpResponse(json.dumps(result_array), 'application/json; charset=UTF-8')
        else:
            return HttpResponse(json.dumps([]), 'application/json; charset=UTF-8')

    def get_queryset(self, **kwargs):
        qs = super(StockListView, self).get_queryset(**kwargs)
        qs = qs.filter(user_id=self.user_id)
        return qs


class StockDetailView(DetailView, APIMixin):
    ADDITIONAL_PARAMS = "&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback"
    model = Stock

    def get(self, request, *args, **kwargs):
        res = super(StockDetailView, self).get(request, *args, **kwargs)
        lastMonth = datetime.date.today().month - 1
        startDate = request.GET.get('startDate', datetime.date.today().replace(month=lastMonth).__str__());
        endDate = request.GET.get('endDate', datetime.date.today().__str__());

        fields = ", ".join(['Date', 'Volume', 'Close'])
        QUERY = ('select %s from yahoo.finance.historicaldata where symbol = "%s" and startDate="%s" and endDate="%s"' % (fields,
                self.object.name, startDate, endDate))
        res = urllib.request.urlopen(self.get_url(QUERY))
        json_res = res.read()
        result_array = self.parse_response_for_object(json_res)

        return HttpResponse(json.dumps(result_array), 'application/json; charset=UTF-8')
