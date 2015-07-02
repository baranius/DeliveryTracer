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

def get_commits(message, comment_pattern):
    results = []

    message = message.replace("\n\ncommit", "\n\n commit")

    messages = message.split("commit")

    for m in messages:
        if len(m) > 1:
            m = "commit " + m

            #get commit id
            commit_pattern = "(commit).*?(\\n)"
            commit_match = re.search(commit_pattern, m)
            commit_id = commit_match.group().replace("\n","").replace("commit ", "")

            #get author
            author_pattern = "(Author).*?(\\n)"
            author_match = re.search(author_pattern, m)
            author = author_match.group().replace("\n","").replace("Author: ", "")

            #get commit message
            comment_pattern = comment_pattern + "(\\n)"
            comment_match = re.search(comment_pattern, m)

            if not comment_match is None:
                comment_message = comment_match.group().replace("\n","")
                result = result_models.LogItem(commit_id, author, comment_message)
                results.append(result)

    resultDictionary = [
        dict(
            commitId = r.get_commit_id(),
            authorInfo = r.get_author(),
            commentText = r.get_comment()
        )
        for r in results
    ]

    return resultDictionary, results
