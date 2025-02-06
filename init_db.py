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

humorists = set()
tags = set()
for humor in humors:
    humorists.update(set(humor['humorists']))
    tags.update(set(humor['tags']))

humorists = sorted(list(humorists))
tags = sorted(list(tags))
humorist_index_dict = {humorists[index]: index for index in range(len(humorists))}
tag_index_dict = {tags[index]: index for index in range(len(tags))}

for i in range(len(humorists)):
    cur.execute("INSERT INTO humorists (id, humorist) VALUES (?, ?)", (i, humorists[i]))

for i in range(len(tags)):
    cur.execute("INSERT INTO tags (id, tag) VALUES (?, ?)", (i, tags[i]))

for humor_index in range(len(humors)):
    humor = humors[humor_index]

    if 'img' in humor:
        img_src = humor['img']['src']
        img_alt = humor['img']['alt']
    else:
        img_src = None
        img_alt = None

    cur.execute("INSERT INTO humors (id, content, censored, img_src, img_alt) VALUES (?, ?, ?, ?, ?)",
                (humor_index, humor['content'], humor['censored'], img_src, img_alt))

    for humorist in humor['humorists']:
        cur.execute("INSERT INTO humor_humorists (humor_id, humorist_id) VALUES (?, ?)",
                    (humor_index, humorist_index_dict[humorist]))

    for tag in humor['tags']:
        cur.execute("INSERT INTO humor_tags (humor_id, tag_id) VALUES (?, ?)",
                    (humor_index, tag_index_dict[tag]))

connection.commit()
connection.close()
