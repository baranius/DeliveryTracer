#imports
import os
import json
import datetime
from core import database, helpers, cmd_factory, git_commands
from flask import Flask, request, g, send_from_directory

#config
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

repo = database.repository(app)

@app.before_request
def before_request():
    if not os.path.exists('delivery_tracer.sqlite'):
        repo.init_db()
    g.db = repo.connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

#Index
@app.route('/')
def index():
    return send_from_directory('','index.html')

#CSS & JS files
@app.route('/content/<file>')
def loadContent(file):
    return send_from_directory('content', file)

@app.route('/templates/<file>')
def loadTemplae(file):
    return send_from_directory('templates', file)

#API Calls
@app.route('/api/GetPipelineList')
def GetPipelineList():
    response = repo.GetPipelineList()
    return json.dumps(response)

@app.route('/api/GetPipelineDetail')
def GetPipelineDetail():
    args = request.args
    name = args.get('p')
    response = repo.GetPipelineDetail(name)
    return json.dumps(response)

@app.route('/api/CreatePipeline')
def CreatePipeline():
    args = request.args
    git_repository = args.get('g')

    if len(git_repository.split('/')) == 0:
        raise ValueError

    project_name = helpers.get_project_name(git_repository)

    commands = cmd_factory.command_factory()
    commands.add(git_commands.clone(git_repository, project_name))
    commands.add(git_commands.log(project_name,""))
    commands.run()

    command_result = {}

    for r in commands.results:
        if r.command is "log":
            command_result = r
            break

    if len(command_result.msg) > 0:
        raise ValueError(command_result.msg)

    output = command_result.output
    (resDict, resObj) = helpers.get_commits(output, args.get('r'))

    for r in resObj:
        repo.CreatePipeline(args.get('p'), args.get('g'), project_name, args.get('r'), args.get('gr'), args.get('bl'), r.get_commit_id())

    return json.dumps({"success":True})

@app.route('/api/UpdatePipeline')
def UpdatePipeline():
    args = request.args
    project_name = args.get('p')
    commit_pattern = args.get('r')
    greenEnv = args.get('gr')
    blueEnv = args.get('bl')

    repo.UpdatePipeline(project_name,commit_pattern, blueEnv, greenEnv)

    return json.dumps({"success":True})

@app.route('/api/DeletePipeline')
def DeletePipeline():
    args = request.args
    pipeline_id = args.get('id')

    repo.DeletePipeline(pipeline_id)

    return json.dumps({"success":True})

@app.route('/api/SaveLog')
def SaveLog():
    args = request.args
    project_name = args.get('p')
    environment = args.get('e')
    version = args.get('v')

    pipeline = repo.GetPipelineDetail(project_name,True)

    factory = cmd_factory.command_factory()
    folder_name = pipeline.get_folder_name()
    last_commit_id = pipeline.get_last_commit_id()

    factory.add(git_commands.log(folder_name, last_commit_id))
    factory.run()

    result = factory.results[0].output

    (response, data) = helpers.get_commits(result, pipeline.get_git_pattern())

    for d in data:
        pipeline_id = pipeline.get_pipeline_id()
        commit_id = d.get_commit_id()
        author_info = d.get_author()
        comment_text = d.get_comment()
        comment_text = comment_text.decode('utf-8')
        date = datetime.date.today().strftime("%d.%m.%Y %H:%M")
        repo.CreateLog(pipeline_id,commit_id,environment,author_info,comment_text,version, date)

    return json.dumps(response)


if __name__ == '__main__':
    app.run()
