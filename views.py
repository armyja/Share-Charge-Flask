# coding=utf-8
from flask import render_template, session, abort, jsonify
import pymysql

from flask import request


def index():
    return render_template('index.html')


def hello(name=None):
    return render_template('hello.html', name=name)


def user():
    if not session.get('logged_in'):
        abort(401)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM USER WHERE USER_NAME = '" + session.get('username') + "'")
    info = jsonify(status="error")
    for i in cur:
        if i:
            _, email, _, username, mobile, student_id, _, sex = i
            info = jsonify(status="success",
                           email=email,
                           username=username,
                           mobile=str(mobile),
                           student_id=str(student_id),
                           sex=sex)
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


def register():
    status = 'no input'
    if request.method == 'POST':
        conn = get_db()
        cur = conn.cursor()
        # todo 防止 SQL 注入
        print(request.form)
        cur.execute(
            "insert into user(email,password,user_name,phone,school_card_id,sex) values (%s,%s,%s,%s,%s,%s);",
            (request.form['email'], request.form['password'], request.form['user_name'],
             request.form['phone'], request.form['school_card_id'], request.form['sex']))
        conn.commit()
        for i in cur:
            if i:
                print(i)
                session['logged_in'] = True
                session['username'] = request.form['user_name']
                status = 'success'
            else:
                status = 'error'
        cur.close()
        conn.close()
    return jsonify(status=status)


def login():
    status = 'Invalid username or password'
    if request.method == 'POST':
        conn = get_db()
        cur = conn.cursor()
        # todo 防止 SQL 注入
        cur.execute("SELECT * FROM USER WHERE USER_NAME = '" + request.form['username'].strip() + "'" +
                    "AND PASSWORD = '" + request.form['password'] + "'")
        for i in cur:
            if i:
                session['logged_in'] = True
                session['username'] = request.form['username']
                status = 'success'
            else:
                status = 'error' + request.form['username'] + ' ' + request.form['password']
        cur.close()
        conn.close()
    return jsonify(status=status)


def logout():
    session.pop('logged_in', None)
    return jsonify(status="success")
