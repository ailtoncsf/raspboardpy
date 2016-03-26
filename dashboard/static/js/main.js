

angular.module('raspboardpyApp', []).config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
})
.controller('dashboardController', ['$scope','$http','$interval', function($scope,$http,$interval) {
  //do banco
  $scope.sensores={};

    $http.get('/api/sensor/tipos').
    success(function(data) {
        $scope.tipos = data;
    });
   

   /* $interval(function(){
      sensores.forEach(function(sensor_id){
        $http.get('/api/sensordata?sensor_id='+sensor_id).
        success(function(data) {
            $scope.instances = data;
        });
      
      })     
    },1000);*/
    $scope.addSensor = function(tipo,portas){
      var __portas = [];
      portas.forEach(function(port){
        __portas.push(port["valor"]);
      })
      $http.get('/api/'+tipo+'?portas='+__portas).
        success(function(sensor_id) {
          $scope.sensores[sensor_id] = {};
          $http.get('/api/sensor?sensor_id='+sensor_id).
            success(function(chart) {
              $scope.sensores[sensor_id] = chart;
                $(chart.chart.renderTo).highcharts(chart);
            });
      });
    }

}]).directive('chart', function() {
    return {
        restrict: 'E',
        template: '<div></div>',
        scope: {
            chartData: "=value",
            chartObj: "=?"
        },
        transclude: true,
        replace: true,
        link: function($scope, $element, $attrs) {

            //Update when charts data changes
            $scope.$watch('chartData', function(value) {
                if (!value)
                    return;

                // Initiate the chartData.chart if it doesn't exist yet
                $scope.chartData.chart = $scope.chartData.chart || {};

                // use default values if nothing is specified in the given settings
                $scope.chartData.chart.renderTo = $scope.chartData.chart.renderTo || $element[0];
                if ($attrs.type)
                    $scope.chartData.chart.type = $scope.chartData.chart.type || $attrs.type;
                if ($attrs.height)
                    $scope.chartData.chart.height = $scope.chartData.chart.height || $attrs.height;
                if ($attrs.width)
                    $scope.chartData.chart.width = $scope.chartData.chart.type || $attrs.width;

                $scope.chartObj = new Highcharts.Chart($scope.chartData);
            });
        }
    };

});
