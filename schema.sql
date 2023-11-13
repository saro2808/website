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