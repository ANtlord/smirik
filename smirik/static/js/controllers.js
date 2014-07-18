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
            console.log(form.serialize());
            $.post(form.attr('action')+form.data('id')+'/', form.serialize(),
                function (data, textStatus, jqXHR) {
                    // success callback
                }
            );
        }
    }]);
