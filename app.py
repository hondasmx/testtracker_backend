from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request

from api.testcase import get_testcase

app = Flask(__name__)


@app.route('/api/testcase/<int:testcase_id>', methods=['GET'])
def get_task(testcase_id):
    testcase = get_testcase(testcase_id)
    if testcase:
        return jsonify(testcase)
    abort(404)


# @app.route('/api/testcase/', methods=['POST'])
# def create_task():
#     if not request.json or not 'title' in request.json:
#         abort(400)
#     task = {
#         'id': tasks[-1]['id'] + 1,
#         'title': request.json['title'],
#         'description': request.json.get('description', ""),
#         'done': False
#     }
#     tasks.append(task)
#     return jsonify({'task': task}), 201


def _make_responce(body):
    response = make_response(jsonify(body))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 404)


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
