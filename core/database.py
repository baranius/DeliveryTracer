import sqlite3
from flask import g
from contextlib import closing

class repository():

    def __init__(self, appReference):
        self.app = appReference

    def connect_db(self):
        return sqlite3.connect(self.app.config['DATABASE'])

    def init_db(self):
        with closing(self.connect_db()) as db:
            with self.app.open_resource('sql_files/pipeline.sql', mode='r') as f:
                db.cursor().executescript(f.read())
                db.commit()
            with self.app.open_resource('sql_files/log.sql', mode='r') as f:
                db.cursor().executescript(f.read())
                db.commit()

    def GetPipelineList(self):
        query = """SELECT
                     Id,
                     PipelineName,
                     GitRepository,
                     GreenEnvironment,
                     BlueEnvironment
                    FROM Pipeline
                    ORDER By PipelineName DESC"""

        cursor = g.db.execute(query)

        response = [
                    dict(
                        Id = row[0],
                        PipelineName = row[1],
                        GitRepository = row[2],
                        GreenEnvironment = row[3],
                        BlueEnvironment = row[4],
                    )
                    for row in cursor.fetchall()
                    ]

        return response

    def GetPipelineDetail(self, name):
        query = """SELECT
                     Id,
                     PipelineName,
                     GitRepository,
                     GitFolderName,
                     CommitPattern,
                     GreenEnvironment,
                     BlueEnvironment,
                     LastCheckedGitCommitId
                    FROM Pipeline
                    WHERE PipelineName = ?"""
        cursor = g.db.execute(query, [name])

        response = [
                    dict(
                        Id = row[0],
                        PipelineName = row[1],
                        GitRepository = row[2],

                        GreenEnvironment = row[3],
                        BlueEnvironment = row[4],
                    )
                    for row in cursor.fetchall()
                    ]
        return response

    def CreatePipeline(self, pipelineName, gitRepository, gitFolderName, commitPattern, greenEnvironment, blueEnvironment, lastCheckedGitCommitId):

        query = """INSERT INTO Pipeline
                        (
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
                             ?,
                             ?,
                             ?,
                             ?,
                             ?,
                             ?,
                             ?
                        )                    """
        cursor = g.db.execute(query, [pipelineName, gitRepository, gitFolderName, commitPattern, \
                                      greenEnvironment, blueEnvironment, lastCheckedGitCommitId])

    def UpdatePipeline(self, pipelineId, pipelineName, commitPattern):
        query = """UPDATE Pipeline
                    SET
                    PipelineName = ?,
                    CommitPattern = ?
                    WHERE Id = ?
                    """
        cursor = g.db.execute(query, [pipelineName, commitPattern, pipelineId])


    def CreateLog(self, pipelineId, commitId, environmentName, author, message, versionString, datetime):
        query = """INSERT INTO Log
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
                             ?,
                             ?,
                             ?,
                             ?,
                             ?,
                             ?,
                             ?
                        )        """

        cursor = g.db.execute(query, [pipelineId, commitId, environmentName, author, message, versionString, datetime])

    def GetLogsByPipelineId(self, pipelineId):
        query = """ SELECT
                     PipelineId     ,
                     CommitId       ,
                     EnvironmentName,
                     Author         ,
                     Message        ,
                     VersionString  ,
                     DateTime
                    FROM Log
                    WHERE PipelineId = ?
                    ORDER By DateTime DESC"""
        cursor = g.db.execute(query, [pipelineId])

        response = [
                    dict(
                        PipelineId = row[0],
                        CommitId = row[1],
                        EnvironmentName = row[2],
                        Author = row[3],
                        Message = row[4],
                        VersionString = row[5],
                        DateTime = row[6]
                    )
                    for row in cursor.fetchall()
                    ]
        return response