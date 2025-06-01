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

DROP TABLE IF EXISTS humorists;

CREATE TABLE humorists (
    id INTEGER PRIMARY KEY,
    humorist TEXT NOT NULL
);

DROP TABLE IF EXISTS tags;

CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    tag TEXT NOT NULL
);

DROP TABLE IF EXISTS viewers;

CREATE TABLE viewers (
    id INTEGER PRIMARY KEY,
    viewer TEXT NOT NULL
);

DROP TABLE IF EXISTS humors;

CREATE TABLE humors (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    censored INTEGER NOT NULL CHECK (censored IN (0, 1)),
    is_local INTEGER NOT NULL CHECK (is_local IN (0, 1)),
    img_src VARCHAR(255),
    img_alt VARCHAR(255)
);

DROP TABLE IF EXISTS humor_humorists;

CREATE TABLE humor_humorists (
    humor_id INTEGER REFERENCES humors(id),
    humorist_id INTEGER REFERENCES humorists(id)
);

DROP TABLE IF EXISTS humor_tags;

CREATE TABLE humor_tags (
    humor_id INTEGER REFERENCES humors(id),
    tag_id INTEGER REFERENCES tags(id)
);

DROP TABLE IF EXISTS humor_viewers;

CREATE TABLE humor_viewers (
    humor_id INTEGER REFERENCES humors(id),
    viewer_id INTEGER REFERENCES viewers(id)
);