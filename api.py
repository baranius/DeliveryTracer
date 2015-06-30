"""
Routes and views for the flask application.
"""
from app import git, command
from PipelineStatsApi.helpers import helpers
from PipelineStatsApi.models import formModels
from datetime import datetime
from flask import render_template, jsonify, request, flash, redirect
from PipelineStatsApi import app


@app.route('/project/log')
def getLatestLog():

    repository = request.args.get('repository')
    if len(repository.split()) == 0:
        raise ValueError

    projectName = helpers.ProjectHelper().getProjectName(repository)

    commandExecutor = git.Git()
    commandExecutor.add(command.Clone(repository, projectName))
    commandExecutor.add(command.Log(projectName))
    commandExecutor.run()

    return jsonify(commandResults=[commandresult.serialize() for commandresult in commandExecutor.results])



@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template('index.html',
        title='Home Page',
        year=datetime.now().year,)

@app.route('/create', methods=['GET', 'POST'])
def create():
    """Renders the contact page."""

    form = formModels.RepositoryForm()
    if form.validate_on_submit():
        flash('Create repository requested for uri="%s", name=%s' %
              (form.uri.data, str(form.name.data)))
        return redirect('/home')

    return render_template('create.html',
                           title='Create Repo',
                           form=form)

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.')
