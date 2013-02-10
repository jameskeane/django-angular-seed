'use strict';

var staticApp = angular.module('staticApp', [])
  .config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
    $locationProvider.html5Mode(true);
    $routeProvider
      .when('/', {
        templateUrl: '/static/views/main.html',
        controller: 'MainCtrl'
      })
      .when('/login', {
        templateUrl: '/static/views/login.html',
        controller: 'LoginCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  }]);

staticApp.directive('activeLink', ['$location', function(location) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs, controller) {
            var clazz = attrs.activeLink;
            var path = $(element).find('a').attr('href');

            scope.location = location;
            scope.$watch('location.path()', function(newPath) {
                if (path === newPath) {
                    element.addClass(clazz);
                } else {
                    element.removeClass(clazz);
                }
            });
        }
    };
}]);