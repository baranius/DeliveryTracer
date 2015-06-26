using System;

namespace DeliveryTracer.DataLayer.DataObjects
{
    public class Pipeline
    {
        public Guid Id { get; set; }
        public string PipelineName { get; set; }
        public string GitRepository { get; set; }
        public string GitFolderName { get; set; }
        public string CommitPattern { get; set; }
        public string GreenEnvironment { get; set; }
        public string BlueEnvironment { get; set; }
        public string LastCheckedGitCommitId { get; set; }
    }
}