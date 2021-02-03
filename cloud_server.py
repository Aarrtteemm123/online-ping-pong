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
    name = request.form.get('name')
    db = get_db()
    db.execute('delete from available_servers where name=?', (name,))
    db.commit()
    return Response('The server was successfully deleted')

@app.route('/connect_to_server',methods=['PUT'])
def connect_to_server():
    name = request.form.get('name')
    db = get_db()
    data = db.execute('select players, max_players from available_servers where name=?',(name,)).fetchall()
    if len(data) == 0:
        return Response('The server does not exist')
    elif data[0][0] == data[0][1]:
        return Response('The server is full')
    elif data[0][0] < data[0][1]:
        db.execute('update available_servers set players=? where name=?',(data[0][0]+1,name))
        db.commit()
        return Response('Ok')
    else:
        res = app.make_response('Unknown error:(')
        res.status_code = 500
        return res

@app.route('/register_server',methods=['POST'])
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
    return Response('The server is successfully registered')

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