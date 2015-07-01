import re
import result_models

def get_project_name(repository_uri):
    strings = repository_uri.split('/')

    projectName = ''
    if len(strings[-1].split()) > 0:
        projectName = strings[-1].replace('.git', '')
    elif  len(strings[-2].split()) > 0:
        projectName = strings[-2].replace('.git', '')

    return projectName

def get_comments(message, comment_pattern):
    results = []

    message = message.replace("\n\ncommit", "\n\n commit")

    messages = message.split("commit")

    for m in messages:
        if len(m) > 1:
            m = "commit " + m

            #get commit id
            commit_pattern = "(commit).*?(\\n)"
            commit_match = re.match(commit_pattern, m)
            commit_id = commit_match.group().replace("\n","").replace("commit ", "")

            #get author
            author_pattern = "(Author).*?(\\n)"
            author_match = re.match(author_pattern, m)
            author = author_match.group().replace("\n","").replace("Author: ", "")

            #get commit message
            comment_match = re.match(comment_pattern, m)
            comment_message = comment_match.group().replace("\n","")

            result = result_models.LogItem(commit_id, author, comment_message)
            results.append(result)

    return results
