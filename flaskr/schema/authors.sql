-- Создание первой базы данных authors_database

CREATE TABLE IF NOT EXISTS author (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL,
    email TEXT NOT NULL
);



CREATE TABLE IF NOT EXISTS blog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER,
    name TEXT NOT NULL,
    description TEXT
    -- FOREIGN KEY (owner_id) REFERENCES author(id)
);


CREATE TABLE IF NOT EXISTS post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    header TEXT NOT NULL,
    text TEXT NOT NULL,
    author_id INTEGER,
    blog_id INTEGER
    -- FOREIGN KEY (author_id) REFERENCES author(id),
    -- FOREIGN KEY (blog_id) REFERENCES blog(id)
);

DELETE FROM post where 1;
DELETE FROM blog where 1;
DELETE FROM author where 1;