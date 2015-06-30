import re

def get_project_name(repository_uri):
    strings = repository_uri.split('/')

    projectName = ''
    if len(strings[-1].split()) > 0:
        projectName = strings[-1].replace('.git', '')
    elif  len(strings[-2].split()) > 0:
        projectName = strings[-2].replace('.git', '')

    return projectName

def get_commit_id(message):
    regex_pattern = "(commit).*?(\\n)"
    matches = re.match(regex_pattern, message)

    return matches.group().replace("\n","")

def get_author(message):
    regex_pattern = "(Author).*?(\\n)"
    matches = re.match(regex_pattern, message)

    return matches.group().replace("\n","")

def get_commit_message(message, patern):
    matches = re.match(patern, message)

    return matches.group().replace("\n","")