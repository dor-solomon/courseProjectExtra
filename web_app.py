from flask import Flask, jsonify
from db_connector import get_user, cmd_args
import os
import signal
from sys import argv

cmd_args(argv)

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


@app.route('/users/get_user_data/<user_id>', methods=['GET'])
def get_user_name(user_id):
    user_name = get_user(user_id)
    if user_name is None:
        return "<H1 id='error'>" 'no such user:'+user_id+"</H1>"
    else:
        return "<H1 id='user'>"+user_name+"</H1>"


@app.route('/stop_server')
def stop_server():
    os.kill(os.getpid(), signal.CTRL_C_EVENT)
    return 'Server stopped'


app.run(host='0.0.0.0', debug=True, port=5001)
