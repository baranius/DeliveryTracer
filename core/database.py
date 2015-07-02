import sqlite3
import result_models
from flask import g
from contextlib import closing

class repository():

    def __init__(self, appReference):
        self.app = appReference

    def connect_db(self):
        return sqlite3.connect('delivery_tracer.sqlite')

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

        g.db.commit()

        response = []

        for row in cursor.fetchall():
            response.append(
                 {
                    'Id' : row[0],
                    'PipelineName' : row[1],
                    'GitRepository' : row[2],
                    'GreenEnvironment' : row[3],
                    'BlueEnvironment' : row[4]
                }
            )

        return response

    def GetPipelineDetail(self, name, asObject=False):
        query = """SELECT
                     Id,
                     PipelineName,
                     GitRepository,
                     CommitPattern,
                     GreenEnvironment,
                     BlueEnvironment,
                     LastCheckedGitCommitId,
                     GitFolderName
                    FROM Pipeline
                    WHERE PipelineName = ?"""
        cursor = g.db.execute(query, [name])

        g.db.commit()

        if asObject:
            for row in cursor.fetchall():
                pipeline = result_models.PipelineItem(row[0], row[7], row[6], row[3])
                return pipeline

        else:
            for row in cursor.fetchall():
                return {
                    "Id": row[0],
                    "PipelineName": row[1],
                    "GitRepository": row[2],
                    "GitCommitPattern": row[3],
                    "GreenEnvironment": row[4],
                    "BlueEnvironment": row[5],
                    "LastCheckedGitCommitId": row[6]
                   }


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
        g.db.execute(query, [pipelineName, gitRepository, gitFolderName, commitPattern, \
                                      greenEnvironment, blueEnvironment, lastCheckedGitCommitId])

        result = g.db.commit()

        return result

    def UpdatePipeline(self, pipelineName, commitPattern, blueEnvironment, greenEnvironment):
        query = """UPDATE Pipeline
                    SET
                    CommitPattern = ?,
                    BlueEnvironment = ?,
                    GreenEnvironment = ?
                    WHERE PipelineName = ?
                    """
        g.db.execute(query, [commitPattern, blueEnvironment, greenEnvironment, pipelineName])
        g.db.commit()


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

        g.db.execute(query, [pipelineId, commitId, environmentName, author, message, versionString, datetime])
        g.db.commit()

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

        g.db.commit()

        response = []

        for row in cursor.fetchall():
            response.append(
                {
                        "PipelineId": row[0],
                        "CommitId": row[1],
                        "EnvironmentName": row[2],
                        "Author": row[3],
                        "Message": row[4],
                        "VersionString": row[5],
                        "DateTime": row[6]
                }
            )
        return response

    def DeletePipeline(self, pipeline_id):
        query = """DELETE FROM Pipeline WHERE Id = ?"""
        g.db.execute(query, [pipeline_id])
        g.db.commit()

        query2 = """DELETE FROM Log WHERE PipelineId = ?"""
        g.db.execute(query2, [pipeline_id])
        g.db.commit()