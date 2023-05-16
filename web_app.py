from flask import Flask
from db_connector import get_user
import os
import signal

app = Flask(__name__)


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


app.run(host='127.0.0.1', debug=True, port=5001)
