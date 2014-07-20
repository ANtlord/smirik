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

        $scope.getStockHistory = function(id){
            $http.get('/stock-detail/'+id+'/').
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
                    jQuery.plot('.plot-times').removeClass('i-hide');
                }).
                error(function(data, status, headers, config) {
                    alert('something wrong');
                }); 
        }
    }]);
