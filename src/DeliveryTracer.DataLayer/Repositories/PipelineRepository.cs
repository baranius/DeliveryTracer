using System;
using System.CodeDom;
using System.Collections.Generic;
using System.Linq;
using Dapper;
using DeliveryTracer.DataLayer.DataObjects;

namespace DeliveryTracer.DataLayer.Repositories
{
    public interface IPipelineRepository
    {
        void Insert(Pipeline pipeline);
        void Update(Pipeline pipeline);
        void Delete(Pipeline pipeline);
        List<Pipeline> GetAll();
        Pipeline GetById(Guid Id);
        Pipeline GetByName(string pipelineName);
    }

    public class PipelineRepository : SqLiteBaseRepository, IPipelineRepository
    {
        public void Insert(Pipeline pipeline)
        {
            using (var cnn = CreateDatabaseConnection())
            {
                cnn.Open();

                pipeline.Id = Guid.NewGuid();
                cnn.Execute(
                    @"INSERT INTO Pipeline
                    (
                         Id,                          
                         PipelineName,
                         GitRepository,
                         GitFolderName,
                         CommitPattern,
                         GreenEnvironment,
                         BlueEnvironment,
                         LastCheckedGitCommitId
                    )
                    VALUES
                    (
                         @Id,                          
                         @PipelineName,
                         @GitRepository,
                         @GitFolderName,
                         @CommitPattern,
                         @GreenEnvironment,
                         @BlueEnvironment,
                         @LastCheckedGitCommitId
                    )                    
                    ", pipeline);

                cnn.Close();
            }
        }
        public void Update(Pipeline pipeline)
        {
            using (var cnn = CreateDatabaseConnection())
            {
                cnn.Open();

                cnn.Execute(
                    @"UPDATE Pipeline 
                    SET
                    PipelineName = @PipelineName,
                    CommitPattern = @CommitPattern
                    WHERE Id = @Id                    
                    ", pipeline);

                cnn.Close();
            }
        }

        public void Delete(Pipeline pipeline)
        {
            using (var cnn = CreateDatabaseConnection())
            {
                cnn.Open();

                cnn.Execute(
                    @"
                        DELETE FROM Pipeline
                        WHERE Id = @Id
                    ", pipeline);

                cnn.Execute(
                    @"
                        DELETE FROM Logs
                        WHERE PipelineId = @Id
                    ", pipeline);

                cnn.Close();
            }
        }

        public List<Pipeline> GetAll()
        {
            List<Pipeline> pipelines;
            using (var cnn = CreateDatabaseConnection())
            {
                cnn.Open();

                pipelines = cnn.Query<Pipeline>(
                    @"
                        SELECT
                         Id,                          
                         PipelineName,
                         GitRepository,
                         GreenEnvironment,
                         BlueEnvironment
                        FROM Pipeline
                        ORDER By PipelineName DESC
                    ").ToList();

                cnn.Close();
            }

            return pipelines;
        }

        public Pipeline GetById(Guid Id)
        {
            Pipeline pipeline;
            using (var cnn = CreateDatabaseConnection())
            {
                cnn.Open();

                pipeline = cnn.Query<Pipeline>(
                    @"
                        SELECT
                         Id,                          
                         PipelineName,
                         GitRepository,
                         GitFolderName,
                         CommitPattern,
                         GreenEnvironment,
                         BlueEnvironment,
                         LastCheckedGitCommitId                
                        FROM Pipeline
                        WHERE Id = @Id                     
                    ", Id).FirstOrDefault();

                cnn.Close();
            }

            return pipeline;
        }

        public Pipeline GetByName(string pipelineName)
        {
            Pipeline pipeline;
            using (var cnn = CreateDatabaseConnection())
            {
                cnn.Open();

                pipeline = cnn.Query<Pipeline>(
                    @"
                        SELECT
                         Id,                          
                         PipelineName,
                         GitRepository,
                         GitFolderName,
                         CommitPattern,
                         GreenEnvironment,
                         BlueEnvironment,
                         LastCheckedGitCommitId                
                        FROM Pipeline
                        WHERE PipelineName = @PipelineName
                    ", new { PipelineName = pipelineName }).FirstOrDefault();

                cnn.Close();
            }

            return pipeline;
        }
    }
}