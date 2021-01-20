# python -m flask run
import sqlite3
from flask import Flask, request, g

app = Flask(__name__)
DATABASE = 'servers.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/delete_server',methods=['DELETE'])
def delete_server():
    name = request.form.get('name')
    ip = request.form.get('ip')
    port = request.form.get('port')
    number_players = request.form.get('number_players')
    max_players = request.form.get('max_players')

@app.route('/connect_to_server',methods=['PUT'])
def connect_to_server():
    name = request.form.get('name')
    ip = request.form.get('ip')
    port = request.form.get('port')
    number_players = request.form.get('number_players')
    max_players = request.form.get('max_players')

@app.route('/register_server',methods=['POST'])
def register_server():
    name = request.form.get('name')
    ip = request.form.get('ip')
    port = request.form.get('port')
    number_players = request.form.get('number_players')
    max_players = request.form.get('max_players')

@app.route('/get_servers',methods=['GET'])
def get_servers():
    pass

@app.route('/',methods=['GET'])
def root():
    return 'Hello, gamers!'

app.run(debug=True)