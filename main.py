import sqlite3
import json

from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
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


def get_humors_by_humorists_and_tags(selected_humorists, selected_tags):
    conn = get_db_connection()
    humorist_placeholders = ', '.join('?' for _ in selected_humorists)
    tag_placeholders = ', '.join('?' for _ in selected_tags)
    humors = conn.execute(
        f'''SELECT * FROM humors WHERE id IN
            (SELECT id FROM humor_humorists
            WHERE humorist IN ({humorist_placeholders})
            GROUP BY humor_humorists.id
            HAVING COUNT(DISTINCT humorist) >= ?
            INTERSECT
            SELECT id FROM humor_tags
            WHERE tag IN ({tag_placeholders})
            GROUP BY humor_tags.id
            HAVING COUNT(DISTINCT tag) >= ?);''',
        list(selected_humorists) + [len(selected_humorists)]
        + list(selected_tags) + [len(selected_tags)]
    )
    humors = [dict(row) for row in humors]
    conn.close()
    if humors is None:
        abort(404)
    return humors


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
    with open('static/json/selected_solutions.json', 'r') as file:
        solutions = json.load(file)['solutions']
    return render_template('mathematics.html', solutions=solutions)


@app.route('/mathematics/<category>/all')
def category_all(category):
    conn = get_db_connection()
    problems = conn.execute('SELECT * FROM problems WHERE category = ?',
                            (category,)).fetchall()
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
    with open('static/json/courses.json', 'r') as file:
        course_categories = json.load(file)['categories']
    return render_template('academic.html', course_categories=course_categories)

@app.route('/writings')
def writings():
    return render_template('writings.html')

@app.route('/humor')
def humor():
    # TODO query to the db for the censored-only humors
    with open('static/json/humors.json', 'r') as file:
        humors = json.load(file)['humors']
    return render_template('humor.html', humors=humors)

@app.route('/humor/search')
def search_humors(humorist=None, tag=None):
    conn = get_db_connection()
    all_humorists = sorted([humorist[0] for humorist in conn.execute("SELECT DISTINCT humorist FROM humor_humorists").fetchall()])
    all_tags = sorted([tag[0] for tag in conn.execute("SELECT DISTINCT tag FROM humor_tags").fetchall()])
    conn.close()
    return render_template('search_humors.html', humorists=all_humorists, tags=all_tags)

@app.route('/get_humors', methods=['GET'])
def get_humors():
    selected_tags = request.args.getlist('tag')
    selected_humorists = request.args.getlist('humorist')
    humors = get_humors_by_humorists_and_tags(selected_humorists, selected_tags)
    return jsonify(humors)