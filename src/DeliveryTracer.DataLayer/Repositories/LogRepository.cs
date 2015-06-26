using System;
using System.Collections.Generic;
using System.Linq;
using Dapper;
using DeliveryTracer.DataLayer.DataObjects;

namespace DeliveryTracer.DataLayer.Repositories
{
    public interface ILogRepository
    {
        void Insert(Log log);
        List<Log> GetByPipelineId(Guid pipelineId);
    }

    public class LogRepository : SqLiteBaseRepository, ILogRepository
    {
        public void Insert(Log log)
        {
            using (var cnn = CreateDatabaseConnection())
            {
                cnn.Open();

                cnn.Execute(
                    @"INSERT INTO Log
                    (
                        PipelineId     ,
                        CommitId       ,
                        EnvironmentName,
                        Author         ,
                        Message        ,
                        VersionString  ,
                        DateTime       
                    )
                    VALUES
                    (
                         @PipelineId     ,
                         @CommitId       ,
                         @EnvironmentName,
                         @Author         ,
                         @Message        ,
                         @VersionString  ,
                         @DateTime       
                    )                    
                    ", log);

                cnn.Close();
            }
        }

        public List<Log> GetByPipelineId(Guid pipelineId)
        {
            List<Log> pipelines;
            using (var cnn = CreateDatabaseConnection())
            {
                cnn.Open();

                pipelines = cnn.Query<Log>(
                    @"
                        SELECT
                         PipelineId     ,
                         CommitId       ,
                         EnvironmentName,
                         Author         ,
                         Message        ,
                         VersionString  ,
                         DateTime                
                        FROM Log
                        WHERE PipelineId = @PipelineId
                        ORDER By DateTime DESC
                    ", new {PipelineId = pipelineId}).ToList();

                cnn.Close();
            }

            return pipelines;
        }

    }
}