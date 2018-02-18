CREATE TABLE "users"
(
    name TEXT,
    password_hash TEXT,
    salt TEXT,
    session_id TEXT,
    session_expiry DATETIME,
    id INTEGER PRIMARY KEY AUTOINCREMENT
);
CREATE UNIQUE INDEX users_id_uindex ON "users" (id);
