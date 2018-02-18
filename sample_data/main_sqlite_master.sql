INSERT INTO sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('table', 'users', 'users', 3, 'CREATE TABLE "users"
(
    name TEXT,
    password_hash TEXT,
    salt TEXT,
    session_id TEXT,
    session_expiry TEXT,
    id INTEGER PRIMARY KEY AUTOINCREMENT
)');
INSERT INTO sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('table', 'sqlite_sequence', 'sqlite_sequence', 2, 'CREATE TABLE sqlite_sequence(name,seq)');
INSERT INTO sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('index', 'users_id_uindex', 'users', 5, 'CREATE UNIQUE INDEX users_id_uindex ON "users" (id)');
INSERT INTO sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('table', 'images', 'images', 7, 'CREATE TABLE "images"
(
    name TEXT,
    path TEXT,
    uid INTEGER,
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    private BOOLEAN DEFAULT 0,
    created DATETIME DEFAULT current_timestamp,
    CONSTRAINT images_users_id_fk FOREIGN KEY (uid) REFERENCES users (id)
)');
INSERT INTO sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('index', 'images_id_uindex', 'images', 4, 'CREATE UNIQUE INDEX images_id_uindex ON "images" (id)');