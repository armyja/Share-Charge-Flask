from flask import render_template, session, abort
import pymysql

from flask import request


def index():
    return 'Index Page'


def hello(name=None):
    return render_template('hello.html', name=name)


def user():
    if not session.get('logged_in'):
        abort(401)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM USER WHERE USER_NAME = '" + session.get('username') + "'")
    info = "get info error"
    for i in cur:
        if i:
            info = i
            break
    cur.close()
    conn.close()
    return info


def get_db():
    return pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           passwd='19961027',
                           db='share_charge',
                           charset='UTF8')


def login():
    error = 'Invalid username or password'
    if request.method == 'POST':
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM USER WHERE USER_NAME = '" + request.form['username'] + "'" +
                    "AND PASSWORD = '" + request.form['password'] + "'")
        for i in cur:
            if i:
                session['logged_in'] = True
                session['username'] = request.form['username']
                error = 'Success'
            else:
                error = 'Invalid username or password' + request.form['username'] + ' ' + request.form['password']
        cur.close()
        conn.close()
    return error


def logout():
    session.pop('logged_in', None)
    return 'Logout success'
