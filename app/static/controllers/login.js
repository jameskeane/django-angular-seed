'use strict';

App.controller('LoginCtrl', function($scope, $http, $location, $rootScope) {
  $scope.login = function() {
    $scope.error = false;
    $scope.loading = true;

    $http.get('/auth', {
      headers: {
        'Authorization': $scope.username + ':' + $scope.password
      }
    }).
    success(function(user, status) {
      $rootScope.user = user;
      App.config(['$httpProvider', function($httpProvider) {   
        $httpProvider.defaults.headers.common['Authorization'] = 'Token ' + user.api_key;
      }]);

      $location.path("/");
    }).
    error(function(data, status) {
      $scope.error = true;
      $scope.loading = false;
    });
  };
});
