class GitCommand:
    """ Holds Git commands console """
    def __init__(self):
        self.commands = []
        self.results = []

    def add(self, command):
        self.commands.append(command)

    def run(self):
        for c in self.commands:
            self.results.append(c.execute())

    def results(self):
        return self.results