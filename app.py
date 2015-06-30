#imports
import os
from core import database, helpers, cmd_factory, git_commands
from flask import Flask, request, g, send_from_directory, jsonify

#config
DATABASE = 'delivery_tracer.sqlite'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

repo = database.repository(app)

@app.before_request
def before_request():
    if not os.path.exists(DATABASE):
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
    return jsonify(response)

@app.route('/api/GetPipelineDetail/<name>')
def GetPipelineDetail(name):
    response = repo.GetPipelineDetail(name)
    return jsonify(response)

@app.route('/api/CreatePipeline')
def CreatePipeline():
    args = request.args
    git_repository = args.get('g')

    if len(git_repository.split('/')) == 0:
        raise ValueError

    project_name = helpers.get_project_name(git_repository)

    commands = cmd_factory.GitCommand()
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

    commit_id = helpers.get_commit_id(command_result.output)

    return commit_id
    #repo.CreatePipeline(args.get('p'), args.get('g'), project_name, args.get('r'), args.get('gr'), args.get('bl'), commit_id)



if __name__ == '__main__':
    app.run()
