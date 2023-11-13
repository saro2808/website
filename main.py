import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_problem(category, id):
    conn = get_db_connection()
    problem = conn.execute('SELECT * FROM problems WHERE category = ? AND id = ?',
                           (category, id)).fetchone()
    conn.close()
    if problem is None:
        abort(404)
    return problem


def get_problem_tags(category, id):
    conn = get_db_connection()
    tags = conn.execute('SELECT tag FROM problem_tags WHERE problem_category = ? and problem_id = ?',
                        (category, id)).fetchall()
    tags = [tag[0] for tag in tags]
    conn.close()
    if tags is None:
        abort(404)
    return tags


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret key'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mathematics/<category>/<int:id>')
def problem(category, id):
    problem = get_problem(category, id)
    tags = get_problem_tags(category, id)
    return render_template('problem.html', problem=problem, tags=tags)


@app.route('/cv')
def cv():
    return render_template('cv.html')


@app.route('/mathematics')
def mathematics():
    return render_template('mathematics.html')


@app.route('/mathematics/<category>/all')
def category_all(category):
    conn = get_db_connection()
    problems = conn.execute('SELECT * FROM problems WHERE category = ?',
                            (category,)
                            ).fetchall()
    tags = []
    for problem in problems:
        tags.append(get_problem_tags(problem['category'], problem['id']))
    conn.close()
    category_name = category[0].upper() + category[1:]
    return render_template('category_all.html', problems=problems, category_name=category_name, tags=tags)


@app.route('/music')
def music():
    return render_template('music.html')


@app.route('/academic')
def academic():
    return render_template('academic.html')
