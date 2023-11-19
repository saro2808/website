import sqlite3
import json

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

with open('static/json/problems.json', 'r') as file:
    problems = json.load(file)['problems']

for problem in problems:
    cur.execute("INSERT INTO problems (category, id, statement, solution) VALUES (?, ?, ?, ?)",
                (problem['category'], problem['id'], problem['statement'], problem['solution'])
                )
    for tag in problem['tags']:
        cur.execute("INSERT INTO problem_tags (problem_category, problem_id, tag) VALUES (?, ?, ?)",
                    (problem['category'], problem['id'], tag))

with open('static/json/humors.json', 'r') as file:
    humors = json.load(file)['humors']

humor_index = 0
for humor in humors:
    cur.execute("INSERT INTO humors (id, content, censored) VALUES (?, ?, ?)",
                (humor_index, humor['content'], humor['censored']))
    for humorist in humor['humorists']:
        cur.execute("INSERT INTO humor_humorists (id, humorist) VALUES (?, ?)",
                    (humor_index, humorist))
    for tag in humor['tags']:
        cur.execute("INSERT INTO humor_tags (id, tag) VALUES (?, ?)",
                    (humor_index, tag))
    humor_index += 1

connection.commit()
connection.close()
