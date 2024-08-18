import sqlite3
import json
import os

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


def get_humors_by_humorists_and_tags(selected_humorists, selected_tags, selected_censor):
    conn = get_db_connection()
    subqueries = []
    params = []
    selected_items = [selected_humorists, selected_tags]
    names = ['humorist', 'tag']
    for i in range(2):
        if selected_items[i]:
            placeholders = ', '.join('?' for _ in selected_items[i])
            subqueries.append(f'''SELECT id FROM humor_{names[i]}s
                               WHERE {names[i]} IN ({placeholders})
                               GROUP BY humor_{names[i]}s.id
                               HAVING COUNT(DISTINCT {names[i]}) >= ?''')
            params += list(selected_items[i]) + [len(selected_items[i])]
    query = '''SELECT * FROM humors
               WHERE 1=1 '''
    if selected_censor == 'censored-only':
        query += 'AND censored = ? '
        params = [1] + params
    if selected_tags or selected_humorists:
        query += f'AND id IN (' + ' INTERSECT '.join(subqueries) + ')'
    query += ';'
    humors = [dict(row) for row in conn.execute(query, params)]
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
    with open('static/json/mathematics.json', 'r', encoding='utf-8') as file:
        loaded = json.load(file)
    solutions = loaded['solutions']
    references = loaded['references']
    return render_template('mathematics.html', solutions=solutions, references=references)


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
    with open('static/json/academic.json', 'r', encoding='utf-8') as file:
        loaded = json.load(file)
    course_categories = loaded['categories']
    references = loaded['references']
    return render_template('academic.html', course_categories=course_categories, references=references)


@app.route('/writings')
def writings():
    return render_template('writings.html')


@app.route('/humor')
def humor():
    # TODO query to the db for the censored-only humors
    with open('static/json/humors.json', 'r', encoding='utf-8') as file:
        humors = json.load(file)['humors']
    humors = [humor for humor in humors if humor['censored']]
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
    selected_censor = request.args.get('censor')
    humors = get_humors_by_humorists_and_tags(selected_humorists, selected_tags, selected_censor)
    return jsonify(humors)


@app.route('/art')
def art():
    files = os.listdir('static/images/art')
    files = [[files[2 * i], files[2 * i + 1]] for i in range(len(files) // 2)]
    if len(files) % 2:
        files += [[files[-1]]]
    return render_template('art.html', files=files)


@app.route('/references')
def references():
    with open('static/json/sites.json', 'r', encoding='utf-8') as file:
        sites = json.load(file)['sites']
    return render_template('references.html', sites=sites)
