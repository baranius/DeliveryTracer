(function() {
    angular.module("ajaxModule", [])
    .factory("requestFactory", function ($http) {

        var urlBase = "/api";
        var factory = {};

        factory.getPipelines = function () {
            return $http.get(urlBase + "/GetPipelineList");
        }

        factory.getPipelineDetail = function(pipelineName) {
            return $http.get(urlBase + "/GetPipelineDetail?p=" + pipelineName);
        }

        factory.createPipeline = function (pipeline, gitAddress, gitPattern, greenEnv, blueEnv) {
            return $http.get(urlBase + "/CreatePipeline?p=" + pipeline + "&g=" + gitAddress + "&r=" + gitPattern + "&gr=" + greenEnv + "&bl=" + blueEnv);
        }

        factory.updatePipeline = function (pipeline, gitPattern, greenEnv, blueEnv) {
            return $http.get(urlBase + "/UpdatePipeline?p=" + pipeline + "&r=" + gitPattern + "&gr=" + greenEnv + "&bl=" + blueEnv);
        }

        factory.deletePipeline = function (pipelineId) {
            return $http.get(urlBase + "/DeletePipeline?id=" + pipelineId);
        }

        factory.getLogs = function (pipelineName) {
            return $http.get(urlBase + "/GetPipelineLogs?p=" + pipelineName);
        }

        return factory;
    });
})();