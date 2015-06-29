#imports
import os
import repository
from flask import Flask, request, g, send_from_directory, jsonify

#config
DATABASE = 'delivery_tracer.sqlite'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

@app.before_request
def before_request():
    repository.init(app)
    if not os.path.exists(DATABASE):
        repository.init_db()
    g.db = repository.connect_db()

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
    response = repository.GetPipelineList()
    return jsonify(response)

@app.route('/api/GetPipelineDetail/<name>')
def GetPipelineDetail(name):
    response = repository.GetPipelineDetail(name)
    return jsonify(response)

@app.route('/api/CreatePipeline')
def CreatePipeline():
    args = request.args
    strngs = args.get('g').split('/')
    gitFolder = strngs[len(strngs) - 1].replace('.git', '')
    #TODO : LastCommitId must be find and implement as last parameter of the function below
    repository.CreatePipeline(args.get('p'), args.get('g'), gitFolder, args.get('r'), args.get('gr'), args.get('bl'), '')

@app.route('/api/UpdatePipeline')
def CreatePipeline():
    args = request.args
    repository.UpdatePipeline(args.get('p'), args.get('r'))

@app.route('/api/CreateLog')
def CreatePipeline():
    args = request.args
    pipeline =  args.get('p')
    environment = args.get('e')
    version = args.get('v')
    #TODO : Git functions (which written by Erman) have to be used


if __name__ == '__main__':
    app.run()
