import sqlite3
import json

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

with open('static/json/problems.json', 'r', encoding='utf-8') as file:
    problems = json.load(file)['problems']

for problem in problems:
    cur.execute("INSERT INTO problems (category, id, statement, solution) VALUES (?, ?, ?, ?)",
                (problem['category'], problem['id'], problem['statement'], problem['solution'])
                )
    for tag in problem['tags']:
        cur.execute("INSERT INTO problem_tags (problem_category, problem_id, tag) VALUES (?, ?, ?)",
                    (problem['category'], problem['id'], tag))

with open('static/json/humors.json', 'r', encoding='utf-8') as file:
    humors = json.load(file)['humors']

humor_index = 0
for humor in humors:
    if 'img' in humor:
        img_src = humor['img']['src']
        img_alt = humor['img']['alt']
    else:
        img_src = None
        img_alt = None
    cur.execute("INSERT INTO humors (id, content, censored, img_src, img_alt) VALUES (?, ?, ?, ?, ?)",
                (humor_index, humor['content'], humor['censored'], img_src, img_alt))
    for humorist in humor['humorists']:
        cur.execute("INSERT INTO humor_humorists (id, humorist) VALUES (?, ?)",
                    (humor_index, humorist))
    for tag in humor['tags']:
        cur.execute("INSERT INTO humor_tags (id, tag) VALUES (?, ?)",
                    (humor_index, tag))
    humor_index += 1

connection.commit()
connection.close()
