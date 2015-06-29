create table Log
(
    Id                          integer primary key autoincrement,
    PipelineId                  integer,
    CommitId                    nvarchar(225),
    EnvironmentName             nvarchar(225),
    Author                      nvarchar(225),
    Message                     nvarchar(500),
    VersionString               nvarchar(225),
    DateTime                    datetime
)