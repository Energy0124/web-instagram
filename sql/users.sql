CREATE TABLE "users"
(
    name TEXT,
    password_hash TEXT,
    salt TEXT,
    session_id TEXT,
    session_expiry TEXT,
    id INTEGER PRIMARY KEY AUTOINCREMENT
);
CREATE UNIQUE INDEX users_id_uindex ON "users" (id);
