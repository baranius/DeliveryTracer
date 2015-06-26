namespace DeliveryTracer.Web.Models
{
    public class AppConfigurations
    {
        public string RepositoryDirPattern { get; set; }
        public string CouchbaseUrl { get; set; }
        public string GitPath { get; set; }
        public string GitUri { get; set; }
        public string BucketName { get; set; }
    }
}