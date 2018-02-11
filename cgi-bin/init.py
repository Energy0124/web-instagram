#!/usr/bin/env python3
import sqlite3

from cgi_helper import print_header

conn = sqlite3.connect('web-instagram.sqlite')
c = conn.cursor()

c.execute('''
DROP TABLE IF EXISTS images;
''')

c.execute('''
DROP TABLE IF EXISTS users;
''')

# Create table
c.execute('''
CREATE TABLE "users"
(
    name TEXT,
    password_hash TEXT,
    salt TEXT,
    session_id TEXT,
    session_expiry TEXT,
    id INTEGER PRIMARY KEY AUTOINCREMENT
);

''')

c.execute('''
CREATE UNIQUE INDEX users_id_uindex ON "users" (id);
''')

c.execute('''
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
''')

c.execute('''
CREATE UNIQUE INDEX images_id_uindex ON images (id);
''')

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

print_header()
print("done")
