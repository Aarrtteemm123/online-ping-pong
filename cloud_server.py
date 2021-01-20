# python -m flask run
import json
import sqlite3
from flask import Flask, request, g, Response

app = Flask(__name__)
DATABASE = 'servers.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_request
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/delete_server',methods=['DELETE'])
def delete_server():
    pass

@app.route('/connect_to_server',methods=['PUT'])
def connect_to_server():
    name = request.form.get('name')
    ip = request.form.get('ip')
    port = request.form.get('port')
    number_players = request.form.get('players')
    max_players = request.form.get('max_players')

@app.route('/register_server',methods=['GET'])
def register_server():
    name = request.form.get('name')
    ip = request.form.get('ip')
    port = request.form.get('port')
    number_players = request.form.get('players')
    max_players = request.form.get('max_players')
    db = get_db()
    try:
        db.execute('insert into available_servers values (?,?,?,?,?)',(name,ip,port,number_players,max_players))
        db.commit()
    except sqlite3.IntegrityError:
        res = app.make_response('Server name is not unique')
        res.status_code = 400
        return res
    except Exception as e:
        res = app.make_response(str(e))
        res.status_code = 500
    return res

@app.route('/get_servers',methods=['GET'])
def get_servers():
    db = get_db()
    cursor = db.execute('select * from available_servers')
    columns = [item[0] for item in cursor.description]
    raw_data = cursor.fetchall()
    data = [dict(zip(columns,row)) for row in raw_data]
    return Response(json.dumps(data, default=lambda x: x.__dict__))

@app.route('/',methods=['GET'])
def root():
    return 'Hello, gamers!'

app.run(debug=True)