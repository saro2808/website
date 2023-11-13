import sqlite3
import json

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

with open('static/text/problems.json', 'r') as file:
    problems = json.load(file)['problems']

for problem in problems:
    cur.execute("INSERT INTO problems (category, id, statement, solution) VALUES (?, ?, ?, ?)",
                (problem['category'], problem['id'], problem['statement'], problem['solution'])
                )
    for tag in problem['tags']:
        cur.execute("INSERT INTO problem_tags (problem_category, problem_id, tag) VALUES (?, ?, ?)",
                    (problem['category'], problem['id'], tag)
                    )

connection.commit()
connection.close()
