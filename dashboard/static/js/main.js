$(document).ready(function() {
  $(chart_id).highcharts({
    chart: chart,
    title: title,
    xAxis: xAxis,
    yAxis: yAxis,
    series: series
  });
});


angular.module('raspboardpyApp', []).config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
})
.controller('dashboardController', ['$scope','$http','$interval', function($scope,$http,$interval) {
  

    $http.get('/api/sensor/tipos').
    success(function(data) {
        $scope.tipos = data;
    });
   
/*
    $interval(function(){
      $http.get('http://localhost:8080/instances').
      success(function(data) {
          $scope.instances = data;
      });
   
    },1000);*/

    $scope.addSensor = function(){
      $http.get('http://localhost:8080/instances/new').
        success(function(data) {
          if (data =="OK"){
            $scope.hassuccess = "Executada com Sucesso."
          }else{
            $scope.haserror = data;
          }
        });
    }
    $scope.execute = function(){
      $http.post('http://localhost:8080/execute?sql=' + $scope.query).
        success(function(data) {
          console.log(data);
          if (data =="OK"){
            $scope.hassuccess = "Executada com Sucesso."
          }else{
            $scope.haserror = data;
          }
        });
    }
     $scope.stop = function(id){
        $http.post('http://localhost:8080/instances/stop/?id=' + id).
        success(function(data) {
          if (data =="OK"){
                $scope.hassuccess = "Executada com Sucesso."
            }else{
            $scope.haserror = data;
            }
        });
    }
   
}]);
