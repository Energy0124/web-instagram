#!/usr/bin/env python3
import cgi
import cgitb
import hashlib
import sqlite3
import uuid
from http import cookies

from cgi_helper import *

cgitb.enable()

form = cgi.FieldStorage()




if "username" not in form or "password" not in form:
    print_header()
    redirect_page()
    print("<H1>Error</H1>")
    print("Please fill in the username and password  fields, redirecting to index in 5 seconds")
else:
    username = form["username"].value
    password = form["password"].value

    conn = sqlite3.connect('web-instagram.sqlite')
    conn.row_factory = sqlite3.Row
    # prepare a cursor object using cursor() method
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE name=?", (username,))
    result = cursor.fetchone()
    if result:
        salt = result['salt']
        hashed_password = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
        password_hash = result['password_hash']

        if hashed_password == password_hash:
            session_id = uuid.uuid4().hex
            cursor.execute("UPDATE users SET session_id = ? WHERE name = ?", (session_id, username,))

            C = cookies.SimpleCookie()
            C["session_id"] = session_id
            C["session_id"]["path"] = "/"
            C["session_id"]["max-age"] = 2147483647
            print_header(C)
            redirect_page()
            print("Successfully login, redirecting to index in 5 seconds")

            conn.commit()
            # We can also close the connection if we are done with it.
            # Just be sure any changes have been committed or they will be lost.
            conn.close()
        else:
            print_header()
            print("incorrect password or username, redirecting to index in 5 seconds")
    else:
        print_header()
        print("incorrect password or username, redirecting to index in 5 seconds")