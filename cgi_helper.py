#!/usr/bin/env python
def print_header(cookie=None):
    print("Content-Type: text/html")  # HTML is following
    if cookie:
        print(cookie)
    print()  # blank line, end of headers


def create_user(cursor, username, password):
    import hashlib, uuid
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
    session_id = uuid.uuid4().hex
    cursor.execute("INSERT INTO users(name, password_hash, salt, session_id, session_expiry) VALUES (?,?,?,?,?)",
                   (username, hashed_password, salt, session_id, None))

    return session_id


def redirect_page():
    print("""
        <meta http-equiv="refresh" content="5;url=index.py">
        """)
