using System;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Web.Http;
using System.Web.Mvc;
using DeliveryTracer.DataLayer.DataObjects;
using DeliveryTracer.DataLayer.Repositories;
using DeliveryTracer.Web.Models.Enums;
using DeliveryTracer.Web.Services;
using Newtonsoft.Json;

namespace DeliveryTracer.Web.Controllers
{
    public class TraceController : ApiController
    {
        private readonly IPipelineRepository _pipelineRepository;
        private readonly ILogRepository _logRepository;
        private readonly IGitService _gitService;
        private readonly RegexService _regexService;

        public TraceController()
        {
            _pipelineRepository = DependencyResolver.Current.GetService<IPipelineRepository>();
            _logRepository = DependencyResolver.Current.GetService<ILogRepository>();
            _gitService = DependencyResolver.Current.GetService<IGitService>();
            _regexService = DependencyResolver.Current.GetService<RegexService>();
        }

        private static HttpResponseMessage Response(string json)
        {
            var response = new HttpResponseMessage
            {
                Content = new StringContent(json)
            };
            response.Content.Headers.ContentType = new MediaTypeHeaderValue("application/json");
            return response;
        }

        [System.Web.Http.HttpGet]
        [System.Web.Http.ActionName("GetPipelineList")]
        public HttpResponseMessage GetPipelineList()
        {
            var pipelines = _pipelineRepository.GetAll();

            return Response(JsonConvert.SerializeObject(pipelines));
        }

        [System.Web.Http.HttpGet]
        [System.Web.Http.ActionName("GetPipelineDetail")]
        public HttpResponseMessage GetPipelineDetail(string p)
        {
            var pipeline = _pipelineRepository.GetByName(p);

            return Response(JsonConvert.SerializeObject(pipeline));

        }

        [System.Web.Http.HttpGet]
        [System.Web.Http.ActionName("GetPipelineLogs")]
        public HttpResponseMessage GetPipelineLogs(string p)
        {
            var pipeline = _pipelineRepository.GetByName(p);

            var logs = _logRepository.GetByPipelineId(pipeline.Id);

            return Response(JsonConvert.SerializeObject(logs));

        }


        [System.Web.Http.HttpGet]
        [System.Web.Http.ActionName("CreatePipeline")]
        public HttpResponseMessage CreatePipeline(string p, string g, string r, string gr, string bl)
        {
            var gitPathSplitted = g.Split('/');

            var pipeline = new Pipeline
            {
                PipelineName = p,
                GitRepository = g,
                GitFolderName = gitPathSplitted.Last().Replace(".git", ""),
                CommitPattern = r,
                GreenEnvironment = gr,
                BlueEnvironment = bl
            };

            _gitService.Process(GitCommand.Clone, pipeline);

            var pullResult = _gitService.Process(GitCommand.Log, pipeline);

            pipeline.LastCheckedGitCommitId = _regexService.GetCommitId(pullResult);

            _pipelineRepository.Insert(pipeline);
            
            return Response(JsonConvert.SerializeObject(new {Success = true}));
        }

        [System.Web.Http.HttpGet]
        [System.Web.Http.ActionName("UpdatePipeline")]
        public HttpResponseMessage UpdatePipeline(string p, string r, string gr, string bl)
        {
            var pipeline = _pipelineRepository.GetByName(p);

            pipeline.CommitPattern = r;
            pipeline.GreenEnvironment = gr;
            pipeline.BlueEnvironment = bl;

            _pipelineRepository.Update(pipeline);

            return Response(JsonConvert.SerializeObject(new { Success = true }));
        }

        [System.Web.Http.HttpGet]
        [System.Web.Http.ActionName("DeletePipeline")]
        public HttpResponseMessage DeletePipeline(string id)
        {
            var pipeline = new Pipeline
            {
                Id = new Guid(id),
            };
            
            _pipelineRepository.Delete(pipeline);

            return Response(JsonConvert.SerializeObject(new { Success = true }));
        }

        [System.Web.Http.HttpGet]
        [System.Web.Http.ActionName("Save")]
        public HttpResponseMessage Save(string p, string e, string v)
        {
            var pipeline = _pipelineRepository.GetByName(p);

            var processResult = _gitService.Process(GitCommand.Log, pipeline);

            var messages = processResult.Split(new[] { "commit " }, 5, StringSplitOptions.RemoveEmptyEntries);

            foreach (var m in messages)
            {
                var log = new Log
                {
                    DateTime = DateTime.Now,
                    VersionString = v,
                    CommitId = _regexService.GetCommitId("commit " + m),
                    Author = _regexService.GetAuthor(m),
                    Message = _regexService.GetComment(pipeline.CommitPattern, m),
                    EnvironmentName = e,
                    PipelineId = pipeline.Id
                };

                _logRepository.Insert(log);
            }

            return Response(JsonConvert.SerializeObject(new { Success = true }));

        }

    }
}
