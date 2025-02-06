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


conn = get_db_connection()

selection_humorists = conn.execute('''SELECT * FROM humorists;''').fetchall()
humorist_id_dict = {row['humorist']: row['id'] for row in selection_humorists}
id_humorist_dict = {row['id']: row['humorist'] for row in selection_humorists}
all_humorists = list(humorist_id_dict.keys())

selection_tags = conn.execute('''SELECT * FROM tags;''').fetchall()
tag_id_dict = {row['tag']: row['id'] for row in selection_tags}
id_tag_dict = {row['id']: row['tag'] for row in selection_tags}
all_tags = list(tag_id_dict.keys())

conn.close()


def get_humors_by_humorists_and_tags(selected_humorists, selected_tags, selected_censor):
    conn = get_db_connection()
    subqueries = []
    params = []

    selected_items = [selected_humorists, selected_tags]
    humorist_ids = [humorist_id_dict[humorist] for humorist in selected_humorists]
    tag_ids = [tag_id_dict[tag] for tag in selected_tags]
    selected_item_ids = [humorist_ids, tag_ids]

    names = ['humorist', 'tag']
    for i in range(2):
        if selected_items[i]:
            placeholders = ', '.join('?' for _ in selected_items[i])
            subqueries.append(f'''SELECT humor_id FROM humor_{names[i]}s
                               WHERE {names[i]}_id IN ({placeholders})
                               GROUP BY humor_{names[i]}s.humor_id
                               HAVING COUNT(DISTINCT {names[i]}_id) >= ?''')
            params += list(selected_item_ids[i]) + [len(selected_item_ids[i])]
    query = '''SELECT * FROM humors
               WHERE 1=1 '''
    if selected_censor == 'censored-only':
        query += 'AND censored = ? '
        params = [1] + params
    if selected_tags or selected_humorists:
        query += f'AND id IN (' + ' INTERSECT '.join(subqueries) + ')'
    query += ';'
    humors = [dict(row) for row in conn.execute(query, params)]

    for humor in humors:
        humor['humorists'] = [row['humorist_id'] for row in conn.execute(f'''SELECT humorist_id FROM humor_humorists
                                                                            WHERE humor_id = {humor["id"]}''')]
        humor['tags'] = [row['tag_id'] for row in conn.execute(f'''SELECT tag_id FROM humor_tags
                                                                    WHERE humor_id = {humor["id"]}''')]
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
    books = loaded['books']
    references = loaded['references']
    return render_template('mathematics.html', solutions=solutions, books=books, references=references)


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
    return render_template('humor.html')


@app.route('/humor/search')
def search_humors():
    return render_template('search_humors.html', humorists=all_humorists, tags=all_tags,
                           id_humorist_dict=id_humorist_dict, id_tag_dict=id_tag_dict, mandatory_tag_list=[])


@app.route('/humor/search-all')
def search_humors_all():
    return render_template('search_humors.html', humorists=all_humorists, tags=all_tags,
                           id_humorist_dict=id_humorist_dict, id_tag_dict=id_tag_dict,
                           mandatory_tag_list=[], non_censored_too=True)


@app.route('/get_humors', methods=['GET'])
def get_humors():
    selected_tags = request.args.getlist('tag')
    selected_humorists = request.args.getlist('humorist')
    selected_censor = request.args.get('censor')
    humors = get_humors_by_humorists_and_tags(selected_humorists, selected_tags, selected_censor)
    return jsonify(humors)


def humor_category(category_tag, non_censored_too=False):
    conn = get_db_connection()
    humorist_ids = [row['humorist_id'] for row in conn.execute(f'''SELECT DISTINCT humorist_id
                                                    FROM humor_humorists JOIN humor_tags
                                                    ON humor_humorists.humor_id = humor_tags.humor_id
                                                    WHERE humor_tags.tag_id = {tag_id_dict[category_tag]};''').fetchall()]
    tag_ids = [row['tag_id'] for row in conn.execute(f'''SELECT DISTINCT t1.tag_id
                                                    FROM humor_tags t1 JOIN humor_tags t2
                                                    ON t1.humor_id = t2.humor_id
                                                    WHERE t2.tag_id = {tag_id_dict[category_tag]};''').fetchall()]
    humorists = [id_humorist_dict[id] for id in humorist_ids]
    tags = [id_tag_dict[id] for id in tag_ids]
    tags.remove(category_tag)  # remove category tag not to let toggling it and loading all humors
    conn.close()
    return render_template('search_humors.html', humorists=humorists, tags=tags,
                           id_humorist_dict=id_humorist_dict, id_tag_dict=id_tag_dict,
                           mandatory_tag_list=[category_tag], non_censored_too=non_censored_too)


@app.route('/humor-isaa')
def humor_isaa():
    return humor_category("ISAA")


@app.route('/humor-isaa-all')
def humor_isaa_all():
    return humor_category("ISAA", non_censored_too=True)


@app.route('/humor-familiar')
def humor_familiar():
    return humor_category("ընտանեկան")


@app.route('/humor-familiar-all')
def humor_familiar_all():
    return humor_category("ընտանեկան", non_censored_too=True)


@app.route('/humor-phystech')
def humor_phystech():
    return humor_category("ֆիզտեխ")


@app.route('/humor-phystech-all')
def humor_phystech_all():
    return humor_category("ֆիզտեխ", non_censored_too=True)


@app.route("/verify_answer", methods=["POST"])
def verify_answer():
    user_answer = request.form.get("answer", "").strip()
    correct = user_answer == "1"  # the answer to the problem
    if correct:
        return render_template("humor.html", correct=True)
    return render_template("humor.html", incorrect=True)


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
