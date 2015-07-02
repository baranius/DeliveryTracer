'use strict';


(function () {

    var app = angular.module('tracerApp', ['ngRoute', 'ajaxModule']);

    app.controller('topMenuController', function () {
        this.pageTitle = document.title;
    });

    app.editPipelineValue = "";

    app.config(function ($routeProvider) {
        $routeProvider
            .when('', {
                templateUrl: 'templates/logs.html',
                controller: 'logsController',
                controllerAs: 'lCtrl'
            })
            .when('/', {
                templateUrl: 'templates/logs.html',
                controller: 'logsController',
                controllerAs: 'lCtrl'
            })
            .when('/pipelines', {
                templateUrl: 'templates/pipelines.html',
                controller: 'pipelineController',
                controllerAs: 'pCtrl'
            })
            .when('/createPipeline', {
                templateUrl: 'templates/create-pipeline.html',
                controller: 'createPipelineController',
                controllerAs: 'cpCtrl'
            })
            .when('/editPipeline/:pipelineName', {
                templateUrl: 'templates/edit-pipeline.html',
                controller: 'editPipelineController',
                controllerAs: 'epCtrl'
            });
    });

    app.controller('logsController', function (requestFactory) {
        var scope = this;
        scope.pipelines = [];
        scope.logs = [];
        scope.greenEnvironmentKey = "";
        scope.blueEnvironmentKey = "";

        requestFactory.getPipelines().success(function (pipelines) {
            scope.pipelines = pipelines;
        });

        scope.selection = function () {
            var index = document.getElementById('pSelect').value;
            
            var pipeline = scope.pipelines[index];
            scope.greenEnvironmentKey = pipeline.GreenEnvironment;
            scope.blueEnvironmentKey = pipeline.BlueEnvironment;

            requestFactory.getLogs(pipeline.PipelineName).success(function (logs) {
                scope.logs = logs;
            });
        };
    });

    app.controller('pipelineController', function (requestFactory) {
        var scope = this;
        scope.pipelines = [];

        requestFactory.getPipelines().success(function (pipelines) {
            scope.pipelines = pipelines;
        });

        scope.createPipeline = function () {
            window.location = "#/createPipeline";
        };

        scope.editPipeline = function (pipelineId) {
            app.editPipelineValue = pipelineId;
        };

        scope.deletePipeline = function (pipelineId) {
            requestFactory.deletePipeline(pipelineId);
            window.location.reload();
        };
    });

    app.controller('createPipelineController', function (requestFactory) {
        var scope = this;

        scope.isSaved = false;

        scope.savePipeline = function () {
            var p = pForm.pipelineName.value;
            var g = pForm.gitRepository.value;
            var r = pForm.gitPattern.value;
            var gr = pForm.greenEnvironment.value;
            var bl = pForm.blueEnvironment.value;

            requestFactory.createPipeline(p, g, r, gr, bl);

            scope.isSaved = true;
        };

        scope.pipelineList = function () {
            window.location = "#/pipelines";
        };

    });

    app.controller('editPipelineController', function (requestFactory, $routeParams) {
        var scope = this;
        var pipelineName = $routeParams.pipelineName;
        scope.pipeline = {};

        requestFactory.getPipelineDetail(pipelineName).success(function (pipeline) {
            scope.pipeline = pipeline;
        });

        scope.updatePipeline = function() {
            var r = pForm.gitPattern.value;
            var gr = pForm.greenEnvironment.value;
            var bl = pForm.blueEnvironment.value;

            requestFactory.updatePipeline(scope.pipeline.PipelineName, r, gr, bl).success(function() {
                window.location = "#/pipelines";
            });
        };

        scope.pipelineList = function () {
            window.location = "#/pipelines";
        };
    });

})();
