import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


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
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    problems = conn.execute('SELECT * FROM problems').fetchall()
    conn.close()
    return render_template('index.html', posts=posts, problems=problems)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/mathematics/<category>/<int:id>')
def problem(category, id):
    problem = get_problem(category, id)
    tags = get_problem_tags(category, id)
    return render_template('problem.html', problem=problem, tags=tags)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/mathematics')
def mathematics():
    return render_template('mathematics.html')


@app.route('/mathematics/<category>/all')
def category_all(category):
    conn = get_db_connection()
    problems = conn.execute('SELECT * FROM problems WHERE category = ?',
                            (category,)
                            ).fetchall()
    conn.close()
    return render_template(f'problems/{category}_all.html', problems=problems)

@app.route('/music')
def music():
    return render_template('music.html')

@app.route('/academic')
def academic():
    return render_template('academic.html')