using System;
using DeliveryTracer.Web.Models;

namespace DeliveryTracer.Web.Helpers
{
    public class ConfigCheckHelper
    {
        public static void Check(AppConfigurations config)
        {
            var type = config.GetType();
            var properties = type.GetProperties();

            foreach (var property in properties)
            {
                var value = property.GetValue(config);
                if(string.IsNullOrEmpty(value.ToString()))
                    throw new Exception(string.Format("\"{0}\" is passed as empty string in appSettings.config file!!!", property.Name));
            }
        }
    }
}