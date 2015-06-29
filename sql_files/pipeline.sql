create table Pipeline
(
    Id                          integer primary key autoincrement,
    PipelineName                nvarchar(225),
    GitRepository               nvarchar(225),
    GitFolderName               nvarchar(225),
    CommitPattern               nvarchar(225),
    GreenEnvironment            nvarchar(225),
    BlueEnvironment             nvarchar(225),
    LastCheckedGitCommitId      nvarchar(225)
)
