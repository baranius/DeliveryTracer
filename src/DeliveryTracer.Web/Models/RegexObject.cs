using System.Text.RegularExpressions;

namespace DeliveryTracer.Web.Models
{
    public class RegexObject
    {
        public string Name { get; set; }
        public Regex Regex { get; set; }
    }
}