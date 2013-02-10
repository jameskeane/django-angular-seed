'use strict';

staticApp.controller('LoginCtrl', function($scope, $http) {
  $scope.login = function() {
    $scope.error = false;
    $scope.loading = true;

    $http.get('/auth', {
      headers: {
        'Authorization': $scope.user + ':' + $scope.password
      }
    }).
    success(function(data, status) {
      window.location = '/';
    }).
    error(function(data, status) {
      $scope.error = true;
      $scope.loading = false;
    });
  }
});
