import sqlite3 
from flask import Flask, request, render_template,g,redirect, url_for,session,flash

DATABASE = 'test2.db'
USERNAME ='admin'
PASSWORD = 'admin'
SECRET_KEY=' this is a secret key!'
app =Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def welcome():
    return '<h1>Welcome to CMPUT 410 - Jinja Lab!</h1>'

@app.route('/task', methods = ['GET', 'POST'])
def task():
    if request.method == 'POST':
        if not session.get('logged_in'):
            abort(401)
        description =request.form['description']
        category = request.form['category']
        priority = request.form['priority']
        idd = request.form['id']
        addTask(category,priority,description,idd)
        flash('New task added')
        return redirect(url_for('task'))
    
    return render_template('show_entries.html', tasks = query_db('select * from tasks'))
def addTask(category,priority,description,idd):
    query_db('insert into tasks values(?,?,?,?)',[category,priority,description,idd],one =True)
    get_db().commit()  
    
    
@app.route('/login', methods=['GET','POST'])
def login():
    error =None
    if request.method =='POST':
        if request.form['username']!=app.config['USERNAME']:
            error = 'invalid username'
        elif request.form['password']!=app.config['PASSWORD']:
            error = 'invalid password'
        else:
            session['logged_in']=True
            flash('You are logged in')
            return redirect(url_for('task'))
    return render_template('login.html', error =error)

def removetask(category,priority,description,idd):
    query_db('delete from tasks where category =? and priority =?and description =? and id=?',[category,priority,description,idd],one =True)
    get_db().commit()
        
@app.route('/logout')
def logout():
    session.pop("logged_in")
    flash("You are logged out!")
    return redirect(url_for('task'))

@app.route('/delete', methods=['POST'])
def delete():
    if not session.get('logged_in'):
        abort(401)
    removetask(request.form['category'],request.form['priority'],request.form['description'],request.form['id'])
    flash('Task was deleted successfully!')
    return redirect(url_for('task'))
    
    
    
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
