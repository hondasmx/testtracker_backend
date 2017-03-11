import datetime
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request

from api.project import get_all_projects, get_project, create_project, update_project_field
from api.testcase import get_testcase, add_testcase, get_last_testcase_index, get_project_testcases, \
    update_testcase_field

app = Flask(__name__)


# testcases
@app.route('/api/testcases/<project>/<int:testcase_id>', methods=['GET'])
def testcase_get(testcase_id, project):
    testcase = get_testcase(testcase_id, project)
    if testcase:
        return _make_responce(testcase)
    else:
        return _make_responce('404 not found')
    # abort(404)


@app.route('/api/testcases/<project>/<int:testcase_id>', methods=['PUT'])
def projects_update(project, testcase_id):
    if not request.json or not 'field' or not 'new_value' in request.json:
        abort(400)
    data = request.json
    field = data['field']
    new_value = data['new_value']
    update_testcase_field(project, testcase_id, field, new_value)
    return _make_responce({'project': project, 'testcase_id': testcase_id, 'field': field, 'new_value': new_value})


@app.route('/api/testcases/<project>', methods=['POST'])
def testcase_create(project):
    if not request.json or not 'title' in request.json:
        abort(400)
    if not 'project' in request.json:
        abort(400)
    testcase = request.json
    testcase['createdTime'] = datetime.datetime.now()
    testcase['lastModifiedTime'] = datetime.datetime.now()
    testcase['lastModifiedBy'] = 'againanov'
    testcase['attributes'] = []
    testcase['steps'] = []
    testcase['description'] = ''
    testcase['preconditions'] = ''
    add_testcase(request.json, project)
    testcase_id = get_last_testcase_index(project)
    return _make_responce({'testcase_id': testcase_id}), 201


@app.route('/api/testcases/<project>', methods=['GET'])
def testcases_get(project):
    testcase = get_project_testcases(project)
    return _make_responce(testcase)


# Project
@app.route('/api/projects/<project>', methods=['GET'])
def project_get(project):
    return _make_responce(get_project(project))


@app.route('/api/projects', methods=['POST'])
def project_create():
    if not request.json or not 'title' in request.json:
        abort(400)
    owner = 'againanov'
    project = request.json
    project['owner'] = owner
    project['createdTime'] = datetime.datetime.now()
    project['lastModifiedTime'] = datetime.datetime.now()
    project['lastModifiedBy'] = owner
    project['roles'] = {
        'admin': [owner],
        'developer': [],
        'manager': [],
        'externalUser': [],
        'qaEngineer': []
    }
    create_project(project, project['title'])
    return _make_responce({'title': project['title']}), 201


@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = get_all_projects()
    return _make_responce(projects)


@app.route('/api/projects/<project>', methods=['PUT'])
def projects_update(project):
    if not request.json or not 'field' or not 'new_value' in request.json:
        abort(400)
    if 'title' in request.json['field']:
        abort(403)
    data = request.json
    field = data['field']
    new_value = data['new_value']
    update_project_field(project, field, new_value)
    return _make_responce({'project': project, 'field': field, 'new_value': new_value})


def _make_responce(body):
    response = make_response(jsonify(body))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


# Errors
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'bad request'}), 404)


@app.errorhandler(401)
def auth_required(error):
    return make_response(jsonify({'error': 'Authorization Required'}), 404)


@app.errorhandler(403)
def permissons(error):
    return make_response(jsonify({'error': "You don't have permissions"}), 404)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run()
