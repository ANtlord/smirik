var MONTH_NAMES = ['янв', 'фев', 'март', 'апр', 'май', 'июнь', 'июль', 'авг', 'сент', 'окт', 'ноя', 'дек'];
angular.module('App.Controllers', []).
    controller('StockCtrl', ['$scope', '$http', function($scope, $http){
        $scope.message = "Загрузка...";
        $scope.stocks = null;

        /*
         *  Method for get data of stocks.
         */
        function getStocks(){
            $http.get('/stock-list/').
                success(function(data, status, headers, config) {
                    if (data.length > 0) {
                        $scope.stocks = data;
                        delete $scope.message;

                        $scope.stock_fields = [];
                        $scope.del_btns = [];

                        for (var prop in data[0]) {
                            if (prop != "pk"){
                                $scope.stock_fields.push(prop);
                            }
                        }
                    } 
                    else $scope.message = "У Вас нет стоков.";
                }).
                error(function(data, status, headers, config) {
                    $scope.message = "Ошибка загрузки данных";
                }).
                then(function(data){
                    // Build query for getting data from YAHOO Fianance.
                    var BASE_URL = "https://query.yahooapis.com/v1/public/yql?q=";
                    var ADDITIONAL_PARAMS = ("&format=json&diagnostics=true&env="
                        +"store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=");
                    var FIELDS = "Symbol,Date,Close";
                    var date = new Date();
                    var END_DATE = date.toISOString().substring(0, 10);
                    var YEAR_MONTHS = 12;
                    date.setMonth(date.getMonth()-YEAR_MONTHS);
                    var START_DATE = date.toISOString().substring(0, 10);
                    var condition = ' startDate = "'+START_DATE+'" and endDate = "'+END_DATE+'"';

                    var companies = [];
                    //var strCompanies = '';
                    var items = {}; // Is container for data for points.
                    var counter = 0;
                    if ($scope.stocks != null) {
                        // Get data and calculate it for every stock.
                        for (var i=0; i < $scope.stocks.length; ++i) {
                            //if (i>0) strCompanies+=',';
                            //strCompanies += ('"' + $scope.stocks[i].Symbol + '"');

                            var url = BASE_URL+encodeURI("select "+FIELDS
                                +' from yahoo.finance.historicaldata'
                                +' where symbol = "'+$scope.stocks[i].Symbol+'" and '
                                +condition)+ADDITIONAL_PARAMS;
                            
                            // Get data from YAHOO finance.
                            $http.get(url).
                                success(function(data, status, headers, config) {
                                    for (var i=0; i<data['query']['results']['quote'].length; ++i){
                                        // Represent data to object, which has fields named by dates.
                                        var KEY = data['query']['results']['quote'][i]['Symbol'];
                                        var DATE = data['query']['results']['quote'][i]['Date'];
                                        var PRICE = data['query']['results']['quote'][i]['Close'];
                                        
                                        if ((DATE in items) == false) items[DATE] = 0;
                                        items[DATE] += parseFloat(PRICE);
                                    }

                                }).
                                error(function(data, status, headers, config) {
                                    alert('Ошибка получения данных с YAHOO Finance');
                                }).
                                then(function(data){
                                    ++counter;
                                    // After all downloadings programm will build plot.
                                    if (counter == $scope.stocks.length-1) {
                                        // Build data for building plot.
                                        var xCaptions = [];
                                        var i=0;
                                        var c=0;
                                        var monthNum = null;
                                        var points = [];
                                        var max = null;
                                        // Calculate sum by fields.
                                        var N = items.length-1;
                                        for (var key in items) {
                                            points.push([c, items[key]]);
                                            if (max == null || max < items[key]) max = items[key];

                                            // Create captions by months for x axis of plot.
                                            var month = key.substring(5,7);
                                            if (monthNum == null || monthNum != month) {
                                                monthNum = month;
                                                xCaptions.push(
                                                    [c, MONTH_NAMES[monthNum-1] + " - " + key.substring(0,4)]
                                                );
                                                //++i;
                                            }
                                            ++c;
                                        }

                                        // Builds plot.
                                        jQuery.plot(jQuery('#portfolio-plot-base'), [points], {
                                            xaxis: {
                                                ticks: xCaptions
                                            }
                                        });
                                    }
                                });
                        }
                        console.log(url);
                        
                    }

                    
                });
        }
        getStocks();

        $scope.currentStockID = null;

        $scope.addStock = function(){
            var form = jQuery('.stock-form');
            jQuery.post(form.attr('action'), form.serialize(),
                function (data, textStatus, jqXHR) {
                    if (data != "OK") {
                        var templateInputs = jQuery(form).find('input');
                        for (var i=0; i<templateInputs.length; ++i){
                            jQuery(templateInputs[i]).css('border-color', '');
                        }
                        for(var key in data) {
                            jQuery('#id_'+key).css('border-color', 'red');
                        }
                    }
                    else {
                        getStocks();

                        var templateInputs = jQuery(form).find('input');
                        jQuery('.form-control').val('');
                    }
                }
            );
        }

        $scope.delStock = function(entryPk){
            var form = jQuery('.del-form-'+entryPk);
            jQuery.post(form.attr('action')+form.data('id')+'/', form.serialize(), function(data){});
            getStocks();
        }

        function _getStockHistory(address) {
            $http.get(address).
                success(function(data, status, headers, config) {
                    var points = [];
                    var xCaptions = [];
                    var max = null;
                    var N = data.length;
                    for (var i=0; i<N; ++i){
                        points.push([i, data[N-1-i].Close]);
                        if (i%3 == 0) xCaptions.push([i, data[N-1-i].Date]);
                        if (max == null) max = data[i].Close;
                        else if (max < data[i].Close) max = data[i].Close;
                    }
                    jQuery.plot(jQuery('#plot-base'), [points], {
                        yaxis: {
                            max: max 
                        },
                        xaxis: {
                            ticks: xCaptions
                        }
                    });
                    jQuery('.plot-times').removeClass('i-hide');
                }).
                error(function(data, status, headers, config) {
                    alert('something wrong');
                });
        }

        $scope.getStockHistoryByDates = function(id, startDate, endDate){
            _getStockHistory('/stock-detail/'+id+'/?startDate='+startDate
                             +'&endDate='+endDate);
        }

        $scope.getStockHistory = function(id){
            _getStockHistory('/stock-detail/'+id+'/');
            $scope.currentStockID = id;
        }
        
        function getLastMonths() {
            var lastMonth = new Date().getMonth();
            var LAST_MONTHS = 12;
            var months = [];
            for (var i=1; i<LAST_MONTHS; ++i){
                var date = new Date('2014-01-01');
                date.setMonth(lastMonth-i);
                var N = date.getMonth();
                var endDate = new Date(date)
                endDate.setMonth(N+1)
                months.push({
                    id: N,
                    label: MONTH_NAMES[N]+" "+date.getFullYear(),
                    startDate: date.toISOString().substring(0, 10),
                    endDate: endDate.toISOString().substring(0, 10)
                });
            }
            return months;
        }
        $scope.months = getLastMonths();

        $scope.porfolioHistory = [];
   
    }]);
