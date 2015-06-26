using System;
using System.Data.SQLite;
using System.IO;
using Dapper;


namespace DeliveryTracer.DataLayer.Repositories
{
    public abstract class SqLiteBaseRepository
    {
        private string _connectionString;

        protected void CreateDatabase()
        {
            _connectionString = "Data Source=" + AppDomain.CurrentDomain.BaseDirectory + "App_Data\\DeliveryTracer.sqlite";

            if (!File.Exists(AppDomain.CurrentDomain.BaseDirectory + "App_Data\\DeliveryTracer.sqlite"))
            {
                using (var cnn = new SQLiteConnection(_connectionString))
                {
                    cnn.Open();
                    cnn.Query(
                        @"
                            create table [Pipeline]
                            (
                                Id                          UNIQUEIDENTIFIER PRIMARY KEY,
                                PipelineName                nvarchar(225),
                                GitRepository               nvarchar(225),
                                GitFolderName               nvarchar(225),
                                CommitPattern               nvarchar(225),
                                GreenEnvironment            nvarchar(225),
                                BlueEnvironment             nvarchar(225),
                                LastCheckedGitCommitId      nvarchar(225)
                            )
                ");

                    cnn.Query(
                        @"
                            create table [Log]
                            (
                                PipelineId                  UNIQUEIDENTIFIER,
                                CommitId                    nvarchar(225),
                                EnvironmentName             nvarchar(225),
                                Author                      nvarchar(225),
                                Message                     nvarchar(500),
                                VersionString               nvarchar(225),
                                DateTime                    datetime
                            )
                        ");
                }
            }
        }

        protected SQLiteConnection CreateDatabaseConnection()
        {
            CreateDatabase();
            return new SQLiteConnection(_connectionString);
        }

    }
}