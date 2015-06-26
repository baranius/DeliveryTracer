using System.Configuration.Abstractions;
using System.IO;
using System.Reflection;
using System.Web.Http;
using System.Web.Mvc;
using System.Web.Routing;
using Autofac;
using Autofac.Integration.Mvc;
using DeliveryTracer.DataLayer.Repositories;
using DeliveryTracer.Web.Helpers;
using DeliveryTracer.Web.Models;
using DeliveryTracer.Web.Services;

namespace DeliveryTracer.Web
{
    public class WebApiApplication : System.Web.HttpApplication
    {
        protected void Application_Start()
        {
            RegisterDependencies();
            AreaRegistration.RegisterAllAreas();
            GlobalConfiguration.Configure(WebApiConfig.Register);
            FilterConfig.RegisterGlobalFilters(GlobalFilters.Filters);
            RouteConfig.RegisterRoutes(RouteTable.Routes);
        }

        protected void RegisterDependencies()
        {
            var builder = new ContainerBuilder();

            var settings = ConfigurationManager.Instance.AppSettings.Map<AppConfigurations>();
            ConfigCheckHelper.Check(settings);

            builder.RegisterInstance(settings).As<AppConfigurations>();

            builder.RegisterType<RegexService>().As<RegexService>().SingleInstance();
            builder.RegisterType<GitService>().As<IGitService>().SingleInstance();
            builder.RegisterType<CouchbaseCacheService>().As<ICouchbaseCacheService>().SingleInstance();

            //Repositories
            builder.RegisterType<PipelineRepository>().As<IPipelineRepository>().SingleInstance();
            builder.RegisterType<LogRepository>().As<ILogRepository>().SingleInstance();

            builder.RegisterControllers(Assembly.GetExecutingAssembly());
            var container = builder.Build();
            
            DependencyResolver.SetResolver(new AutofacDependencyResolver(container));
        }
    }
}
