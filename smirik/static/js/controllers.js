angular.module('App.Controllers', []).
    controller('StockCtrl', ['$scope', '$http', function($scope, $http){
        $scope.message = "Загрузка...";
        $http.get('/stock-list/').
            success(function(data, status, headers, config) {
                if (data.length > 0) {
                    $scope.stocks = data;
                    delete $scope.message;

                    $scope.stock_fields = [];
                    for (var prop in data[0]) {
                        $scope.stock_fields.push(prop);
                    }
                } 
                else $scope.message = "У Вас нет стоков.";
            }).
            error(function(data, status, headers, config) {
                $scope.message = "Ошибка загрузки данных";
            });
    }]);
