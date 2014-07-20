angular.module('App.Controllers', []).
    controller('StockCtrl', ['$scope', '$http', function($scope, $http){
        $scope.message = "Загрузка...";
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
                        for (var i=0; i<templateInputs.length; ++i){
                            jQuery(templateInputs[i]).val('');
                        }
                    }
                }
            );
        }

        $scope.delStock = function(entryPk){
            var form = jQuery('.del-form-'+entryPk);
            $.post(form.attr('action')+form.data('id')+'/', form.serialize(), function(data){});
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
        
        MONTH_NAMES = ['янв', 'фев', 'март', 'апр', 'май', 'июнь', 'июль', 'авг', 'сент', 'окт', 'ноя', 'дек'];
        function getLastMonths() {
            var lastMonth = new Date().getMonth();
            var LAST_MONTHS = 12;
            var months = [];
            for (var i=1; i<LAST_MONTHS; ++i){
                var date = new Date('2014-'+lastMonth+'-1');
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
            console.log(months);
            return months;
        }
        $scope.months = getLastMonths();
    }]);
