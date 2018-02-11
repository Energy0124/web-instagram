CREATE TABLE "images"
(
    name TEXT,
    path TEXT,
    uid INTEGER,
    created DATETIME DEFAULT current_time,
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    private BOOLEAN DEFAULT 0,
    CONSTRAINT images_users_id_fk FOREIGN KEY (uid) REFERENCES users (id)
);
CREATE UNIQUE INDEX images_id_uindex ON images (id);
