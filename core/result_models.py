class CommandResult:
    def __init__(self, command, out, msg):
        self.command = command
        self.msg = msg
        self.output = out

    def serialize(self):
        return {
            'command': self.command,
            'output': self.output,
            'msg': self.msg,
        }

    def output(self):
        return self.output

    def msg(self):
        return self.msg

    def command(self):
        return self.command

class PipelineItem:
    def __init__(self, folderName, lastCommitId, gitPattern):
        self.folder_name = folderName
        self.last_commit_id = lastCommitId
        self.git_pattern = gitPattern

    def get_folder_name(self):
        return self.folder_name

    def get_last_commit_id(self):
        return self.last_commit_id

    def get_git_pattern(self):
        return self.git_pattern

class LogItem:
    def __init__(self, commitId, author, comment):
        self.commit_id = commitId
        self.author = author
        self.comment = comment

    def get_commit_id(self):
        return self.commit_id

    def get_author(self):
        return self.author

    def get_comment(self):
        return self.comment