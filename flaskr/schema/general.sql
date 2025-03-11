-- Создание второй базы данных general_database

CREATE TABLE IF NOT EXISTS space_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS event_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    space_type_id INTEGER,
    event_type_id INTEGER,
    FOREIGN KEY (space_type_id) REFERENCES space_type(id),
    FOREIGN KEY (event_type_id) REFERENCES event_type(id)
);

DELETE FROM space_type;
DELETE FROM event_type;

-- Вставка типов пространств
INSERT INTO space_type (id, type) VALUES (1, 'global'), (2, 'blog'), (3, 'post');

-- Вставка типов событий
INSERT INTO event_type (id, type) VALUES (1, 'login'), (2, 'logout'), (3, 'create_post'), (4, 'delete_post'), (5, 'comment');
