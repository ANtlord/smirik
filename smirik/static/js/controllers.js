var app = angular.module('App.Controllers', ['ngResource']);
var StockController = function($scope, $http){
    $http.post(url: '/stock-list/').
        success(function(data, status, headers, config) {
            $scope.stocks = data;
        });
}
app.controller('StockController', StockController);
