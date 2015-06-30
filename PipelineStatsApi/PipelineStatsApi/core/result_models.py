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