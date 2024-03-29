#!/usr/bin/env python
import hashlib
import os
import sqlite3
import uuid
from http import cookies

from pathlib import Path

conn = None


def get_cursor():
    global conn
    conn = sqlite3.connect('web-instagram.sqlite')
    conn.row_factory = sqlite3.Row
    # prepare a cursor object using cursor() method
    cursor = conn.cursor()
    return cursor


def close_db(connection=conn):
    if connection:
        connection.commit()
        connection.close()


def print_header(cookie=None):
    print("Content-Type: text/html")  # HTML is following
    if cookie:
        print(cookie)
    print()  # blank line, end of headers


def get_uuid():
    return uuid.uuid4().hex


def create_user(cursor, username, password):
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
    session_id = uuid.uuid4().hex
    cursor.execute("INSERT INTO users(name, password_hash, salt, session_id) VALUES (?,?,?,?)",
                   (username, hashed_password, salt, session_id))

    return session_id


def redirect_page():
    print("""
        <meta http-equiv="refresh" content="3;url=index.py">
        """)


def get_cookie(key):
    http_cookie = os.environ["HTTP_COOKIE"]
    C = cookies.SimpleCookie()
    C.load(http_cookie)
    if key not in C:
        return None
    value = C[key].value
    return value


def get_clear_cookie():
    C = cookies.SimpleCookie()
    C["session_id"] = ""
    C["session_id"]["path"] = "/"
    C["session_id"]["max-age"] = -1
    return C


def get_images(uid=-1):
    connection = sqlite3.connect('web-instagram.sqlite')
    connection.row_factory = sqlite3.Row
    # prepare a cursor object using cursor() method
    cursor = connection.cursor()
    if uid >= 0:
        cursor.execute("SELECT * FROM images WHERE uid=? OR private=0 ORDER BY created DESC ", (uid,))
    else:
        cursor.execute("SELECT * FROM images WHERE private=0 ORDER BY created DESC ")
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def get_current_user():
    """
get the current logged in user

    :return: row, have session?
    """
    http_cookie = os.environ["HTTP_COOKIE"]
    C = cookies.SimpleCookie()
    C.load(http_cookie)
    if "session_id" not in C:
        return None, False
    session_id = C["session_id"].value
    conn = sqlite3.connect('web-instagram.sqlite')
    conn.row_factory = sqlite3.Row
    # prepare a cursor object using cursor() method
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE session_id=?", (session_id,))
    result = cursor.fetchone()
    conn.commit()
    conn.close()
    if result is None:
        return None, True
    else:
        return result, True


def image_exist(image_name):
    cursor = get_cursor()
    cursor.execute("""
                SELECT  * FROM images WHERE name=?
                """, (image_name,))
    result = cursor.fetchone()

    close_db(cursor.connection)
    if result:
        return result
    else:
        return False


def image_belongs_to(image_name, username):
    cursor = get_cursor()
    cursor.execute("""
                   SELECT  * FROM images JOIN users ON uid=users.id
                   WHERE  images.name=? AND users.name=?
                   """, (image_name,))
    result = cursor.fetchone()

    close_db(cursor.connection)
    if result:
        return result
    else:
        return False


def reset_all_tables():
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
    session_expiry DATETIME,
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
    created DATETIME DEFAULT current_timestamp,
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


# reset_table()
def clear_images_db():
    conn = sqlite3.connect('web-instagram.sqlite')
    c = conn.cursor()
    c.execute('''
    DROP TABLE IF EXISTS images;
    ''')

    c.execute('''
    CREATE TABLE "images"
    (
        name TEXT,
        path TEXT,
        uid INTEGER,
        created DATETIME DEFAULT current_timestamp,
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


def delete_all_images():
    for p in Path(UPLOAD_DIR).glob('*.jpg'):
        p.unlink()
    for p in Path(UPLOAD_DIR).glob('*.jpeg'):
        p.unlink()
    for p in Path(UPLOAD_DIR).glob('*.png'):
        p.unlink()
    for p in Path(UPLOAD_DIR).glob('*.gif'):
        p.unlink()


TO_INDEX_IN_SECONDS = "incorrect password or username, redirecting to index in 3 seconds"
UPLOAD_DIR = './upload'
WEB_UPLOAD_DIR = '/upload'
