#import commands
import subprocess
import os
import sys
import result_models, settings

config = settings._Const()

class command:
    def execute(self): pass

class clone(command):
    """ representation of git clone command """
    def __init__(self, repositoryUri, projectName):
        self.repositoryUri = repositoryUri
        self.projectName = projectName

    def execute(self):
        try:
            if not os.path.exists(config.TEMP_PATH()):
                os.makedirs(config.TEMP_PATH())

            if(os.path.exists(os.path.join(config.TEMP_PATH(), self.projectName))):
                return result_models.CommandResult(clone.__name__, "", "Project {0} has already been cloned before! Skipping this command".format(self.projectName))

            pr = subprocess\
                    .Popen( 'git clone {0}'.format(self.repositoryUri) ,\
                             cwd = os.path.dirname( config.TEMP_PATH() ),\
                             shell = True, \
                             stdout = subprocess.PIPE,\
                             stderr = subprocess.PIPE )
            (out, msg) = pr.communicate()
            return result_models.CommandResult(clone.__name__, out, msg)

        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise


class log(command):
    """ representation of git log command """

    def __init__(self, projectName, lastCommitId):
        self.project_name = projectName
        self.last_commit_id = lastCommitId

    def execute(self):
        try:
            if len(self.last_commit_id) > 0:
                self.log_command = 'git log {0}^..HEAD'.format(self.last_commit_id)
            else:
                self.log_command = 'git log -1'

            pr = subprocess\
                    .Popen( self.log_command,\
                             cwd = config.PROJECT_PATH(self.project_name),\
                             shell = True, \
                             stdout = subprocess.PIPE,\
                             stderr = subprocess.PIPE )

            (out, msg) = pr.communicate()
            return result_models.CommandResult(log.__name__, out, msg)

        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise


class status(command):
    def execute(self):
        print("git status has been executed.")

class pull(command):
    def __init__(self, project_name):
        self.project_name = project_name

    def execute(self):
        try:
            if not os.path.exists(config.PROJECT_PATH(self.project_name)):
                print "Project folder not found"
                raise

            pr = subprocess\
                    .Popen( 'git pull' ,\
                             cwd = config.PROJECT_PATH(self.project_name),\
                             shell = True, \
                             stdout = subprocess.PIPE,\
                             stderr = subprocess.PIPE )
            (out, msg) = pr.communicate()
            return result_models.CommandResult(clone.__name__, out, msg)

        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise