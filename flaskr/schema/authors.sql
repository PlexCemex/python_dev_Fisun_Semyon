-- Создание первой базы данных authors_database

DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS blog;
DROP TABLE IF EXISTS author;
DROP TABLE IF EXISTS comment;

-- DELETE FROM post;
-- DELETE FROM blog;
-- DELETE FROM author;

CREATE TABLE IF NOT EXISTS author (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS blog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER,
    name TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (owner_id) REFERENCES author(id)
);

CREATE TABLE IF NOT EXISTS post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    header TEXT NOT NULL,
    text TEXT NOT NULL,
    author_id INTEGER,
    blog_id INTEGER,
    FOREIGN KEY (author_id) REFERENCES author(id),
    FOREIGN KEY (blog_id) REFERENCES blog(id)
);

CREATE TABLE IF NOT EXISTS comment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    author_id INTEGER,
    post_id INTEGER,
    FOREIGN KEY (author_id) REFERENCES author(id),
    FOREIGN KEY (post_id) REFERENCES post(id)
);