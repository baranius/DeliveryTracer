using DeliveryTracer.DataLayer.DataObjects;
using DeliveryTracer.Web.Models;
using DeliveryTracer.Web.Models.Enums;

namespace DeliveryTracer.Web.Services
{
    public interface IGitService
    {
        string Process(GitCommand command, Pipeline model);
    }

    public class GitService : IGitService
    {
        private readonly AppConfigurations _config;

        public GitService(AppConfigurations config)
        {
            _config = config;
        }

        public string Process(GitCommand command, Pipeline model)
        {
            return ProcessService.CreateProcessInfo(_config).Run(command, model);
        }
    }
}