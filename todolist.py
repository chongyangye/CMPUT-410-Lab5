import sqlite3 
from flask import Flask, request, render_template,g

DATABASE = 'test.db'


app =Flask(__name__)



@app.route('/')
def welcome():
    return '<h1>Welcome to CMPUT 410 - Jinja Lab!</h1>'

@app.route('/task', methods = ['GET', 'POST'])
def task():
    #if request.method == 'POST':
    
    return render_template('show_entries.html', tasks = query_db('select * from tasks'))

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html', tasks = query_db('select * from tasks'))


def query_db(query, args=(), one=False):
    cur = get_db().cursor()
    cur.execute(query, args)
    r = cur.fetchall()
    cur.close()
    return (r[0] if r else None) if one else r

def get_db():
    db= getattr(g,'_database',None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g,'_database', None)
    if db is not None:
        db.close()
        db=None


if __name__ == '__main__':
    app.debug = True
    app.run()
