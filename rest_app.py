import os
import signal
from sys import argv
from db_connector import DBfunc
from flask import Flask, request, jsonify

args = argv
db = DBfunc(args[1], args[1], args[2], args[3])

app = Flask(__name__)


class InvalidUsage(Exception):
    status_code = 404

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/users/<user_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def user(user_id):
    if request.method == 'GET':
        user_name = db.get_user(user_id)
        if user_name is None:
            return {'status': 'error', 'reason': 'no such id'}, 500
        else:
            return {'status': 'ok', 'user_name': user_name}, 200

    elif request.method == 'POST':
        request_data = request.json
        user_name = request_data.get('user_name')
        try:
            db.add_user(user_id, user_name)
            return {'status': 'ok', 'user_added': user_name}, 200
        except:
            return {'status': 'error', 'reason': "id already exists"}, 500

    elif request.method == 'PUT':
        request_data = request.json
        user_name = request_data.get('user_name')
        updated = db.get_user(user_id)
        if updated is None:
            return {'status': 'error', 'reason': 'no such id'}, 500
        else:
            db.update_user(user_id, user_name)
            return {'status': 'ok', 'user_updated': user_name}, 200

    elif request.method == 'DELETE':
        deleted = db.get_user(user_id)
        if deleted is None:
            return {'status': 'error', 'reason': 'no such id'}, 500
        else:
            db.delete_user(user_id)
            return {'status': 'ok', 'user_deleted': user_id}, 200


@app.route('/stop_server')
def stop_server():
    os.kill(os.getpid(), signal.CTRL_C_EVENT)
    return 'Server stopped'


app.run(host='0.0.0.0', debug=True, port=5000)
