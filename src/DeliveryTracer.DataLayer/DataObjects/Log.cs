using System;

namespace DeliveryTracer.DataLayer.DataObjects
{
    public class Log
    {
        public Guid PipelineId { get; set; }
        public string EnvironmentName { get; set; }
        public string CommitId { get; set; }
        public string Author { get; set; }
        public string Message { get; set; }
        public string VersionString { get; set; }
        public DateTime DateTime { get; set; }
        public string DateTimeString { get { return DateTime.ToString(); } }
    }
}