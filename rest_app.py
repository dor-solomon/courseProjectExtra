from flask import Flask, request
from db_connector import add_user, get_user, update_user, delete_user, cmd_args
import os
import signal
from sys import argv

cmd_args(argv)

app = Flask(__name__)


@app.route('/users/<user_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def user(user_id):
    if request.method == 'GET':
        user_name = get_user(user_id)
        if user_name is None:
            return {'status': 'error', 'reason': 'no such id'}, 500
        else:
            return {'status': 'ok', 'user_name': user_name}, 200

    elif request.method == 'POST':
        request_data = request.json
        user_name = request_data.get('user_name')
        try:
            add_user(user_id, user_name)
            return {'status': 'ok', 'user_added': user_name}, 200
        except:
            return {'status': 'error', 'reason': "id already exists"}, 500

    elif request.method == 'PUT':
        request_data = request.json
        user_name = request_data.get('user_name')
        updated = get_user(user_id)
        if updated is None:
            return {'status': 'error', 'reason': 'no such id'}, 500
        else:
            update_user(user_id, user_name)
            return {'status': 'ok', 'user_updated': user_name}, 200

    elif request.method == 'DELETE':
        deleted = get_user(user_id)
        if deleted is None:
            return {'status': 'error', 'reason': 'no such id'}, 500
        else:
            delete_user(user_id)
            return {'status': 'ok', 'user_deleted': user_id}, 200


@app.route('/stop_server')
def stop_server():
    os.kill(os.getpid(), signal.CTRL_C_EVENT)
    return 'Server stopped'


app.run(host='127.0.0.1', debug=True, port=5000)
