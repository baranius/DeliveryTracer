
class ProjectHelper:
    
    def getProjectName(self, repository):
        splitedRepository = repository.split('/')
    
        projectName = ''
        if len(splitedRepository[-1].split()) > 0:
            projectName = splitedRepository[-1].replace('.git', '')
        elif  len(splitedRepository[-2].split()) > 0:
            projectName = splitedRepository[-2].replace('.git', '')

        return projectName