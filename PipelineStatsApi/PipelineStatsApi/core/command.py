import commands
import subprocess
import os
import sys
import shutil
from   PipelineStatsApi.core import result_models, settings
config = settings._Const()

class Command:
    def execute(self): pass

class Clone(Command):
    """ representation of git clone command """
    def __init__(self, repositoryUri, projectName):
        self.repositoryUri = repositoryUri
        self.projectName = projectName

    def execute(self):
        try:
            if not os.path.exists(config.TEMP_PATH()):
                os.makedirs(config.TEMP_PATH())

            if(os.path.exists(os.path.join(config.TEMP_PATH(), self.projectName))):
                return result_models.CommandResult(Clone.__name__, "", "Project {0} has already been cloned before! Skipping this command".format(self.projectName))
            
            pr = subprocess\
                    .Popen( [config.GIT_DIR(), 'clone', self.repositoryUri],\
                             cwd = os.path.dirname( config.TEMP_PATH() ),\
                             shell = True, \
                             stdout = subprocess.PIPE,\
                             stderr = subprocess.PIPE )
            (out, msg) = pr.communicate()
            return result_models.CommandResult(Clone.__name__, out, msg)

        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise


class Log(Command):
    """ representation of git log command """

    def __init__(self, projectName):
        self.projectName = projectName

    def execute(self):
        try:
            pr = subprocess\
                    .Popen( [config.GIT_DIR(), 'log'],\
                             cwd = os.path.dirname( os.path.join(config.TEMP_PATH(), self.projectName)+"\\" ),\
                             shell = True, \
                             stdout = subprocess.PIPE,\
                             stderr = subprocess.PIPE )

            (out, msg) = pr.communicate()
            return result_models.CommandResult(Log.__name__, out, msg)

        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise


class Status(Command):
    def execute(self):
        print("git status has been executed.")

class Pull(Command):
    def execute(self):
        print("git pull has been executed.")