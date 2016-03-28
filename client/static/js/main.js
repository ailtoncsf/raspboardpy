

angular.module('raspboardpyApp', []).config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
})
.controller('dashboardController', ['$scope','$http','$interval', function($scope,$http,$interval) {



  //do banco
    var MAX_INTERVAL = 3000; //3 segundos
    $scope.sensores= {};
   /***************** TESTANDO SOCKETS ***********************/ 
  var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
        socket.emit('my event', {data: 'I\'m connected!'});
    });

   socket.on('response_api_sensor_chart', function(chart){
             console.log("Grafico vindo por callback:" + chart)
             /*$scope.sensores[sensor_id].chart = chart;
             $scope.sensores[sensor_id].maxinterval = MAX_INTERVAL/1000; 
             $scope.sensores[sensor_id].interval = "";*/
   });
  /***************** TESTANDO SOCKETS ***********************/
    function configSensor(list){
       list.forEach(function(sensor_id){
          $scope.sensores[sensor_id] = {chart:"",interval:null, maxinterval:MAX_INTERVAL/1000};
          setRealTimeChart(sensor_id);
        })
    }


    function setRealTimeChart(sensor_id){
      if (!$scope.sensores.hasOwnProperty(sensor_id)) return;

        var inter = $interval(function(){
              if (!$scope.sensores.hasOwnProperty(sensor_id)) return;
              if ($scope.sensores[sensor_id].maxinterval > 0){
                $scope.sensores[sensor_id].maxinterval--;
              }else{
                  $http.get('/api/sensor/chart?sensor_id='+sensor_id).success(function(chart) {
                  $scope.sensores[sensor_id].chart = chart;
                  $scope.sensores[sensor_id].maxinterval = MAX_INTERVAL/1000;
                });
              }
       },MAX_INTERVAL);
        $scope.sensores[sensor_id].interval = inter;
    }

    $http.get('/api/sensor/tipos').success(function(data) {$scope.tipos = data;});
    $http.get('/api/sensor/listall').success(configSensor);


    $scope.addSensor = function(key,value){
     var _get ="?"
        _get += key ? "tipo=" + key : "";
        _get += value.data ? "&data=" +  value.data : "";
        _get += value.echo ? "&echo=" +  value.echo : "";
        _get += value.trigger ? "&trigger=" +  value.trigger : "";
        $http.get('/api/sensor/start' + _get).success(function(sensor_id){ return configSensor([sensor_id])});
    }

    $scope.removeSensor = function(sensor_id){
      if (!$scope.sensores.hasOwnProperty(sensor_id)) return;
      $interval.cancel($scope.sensores[sensor_id].interval);
      
      $http.get('/api/sensor/stop?sensor_id='+sensor_id).
      success(function(list) {
          delete $scope.sensores[sensor_id];
          configSensor(list)
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

          
                Highcharts.setOptions({
                      plotOptions: {
                          line : {
                            animation : {
                                duration : 0
                            }
                          },
                          bar : {
                            animation : {
                                duration : 0
                            }
                          }
                      }
                  });
                 $scope.chartObj = new Highcharts.Chart($scope.chartData);

            });
        }
    };

});
