DROP TABLE IF EXISTS problems;

CREATE TABLE problems (
    category TEXT,
    id INTEGER,
    statement TEXT NOT NULL,
    solution TEXT NOT NULL,
    PRIMARY KEY (category, id)
);

DROP TABLE IF EXISTS problem_tags;

CREATE TABLE problem_tags (
    problem_category TEXT REFERENCES problems(category),
    problem_id INTEGER REFERENCES problems(id),
    tag VARCHAR(255)
);

DROP TABLE IF EXISTS humors;

CREATE TABLE humors (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    censored INTEGER NOT NULL CHECK (censored IN (0, 1)),
    img_src VARCHAR(255),
    img_alt VARCHAR(255)
);

DROP TABLE IF EXISTS humor_humorists;

CREATE TABLE humor_humorists (
    id INTEGER REFERENCES humors(id),
    humorist VARCHAR(255)
);

DROP TABLE IF EXISTS humor_tags;

CREATE TABLE humor_tags (
    id INTEGER REFERENCES humors(id),
    tag VARCHAR(255)
);