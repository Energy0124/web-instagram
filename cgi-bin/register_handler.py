#!/usr/bin/env python3
import cgi
import cgitb
import html

from cgi_helper import *

cgitb.enable()

form = cgi.FieldStorage()

if "username" not in form or "password" not in form or "confirm_password" not in form:
    print_header()
    redirect_page()
    print("<H1>Error</H1>")
    print("Please fill in the username, password and confirm_password fields, redirecting to index in 3 seconds")
    print("<a href='index.py'>Home</a>")
else:
    username = form["username"].value
    username = html.escape(username)
    password = form["password"].value
    confirm_password = form["confirm_password"].value
    # print("<p>username:", form["username"].value)
    # print("<p>password:", form["password"].value)
    # print("<p>confirm_password:", form["confirm_password"].value)
    if confirm_password == password:

        conn = sqlite3.connect('web-instagram.sqlite')
        # prepare a cursor object using cursor() method
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE name=?", (username,))
        result = cursor.fetchall()
        if len(result) <= 0:
            session_id = create_user(cursor, username, password)
            C = cookies.SimpleCookie()
            C["session_id"] = session_id
            C["session_id"]["path"] = "/"
            C["session_id"]["max-age"] = 2147483647
            print_header(C)
            redirect_page()
            print("Successfully registered, redirecting to index in 3 seconds")
            print("<a href='index.py'>Home</a>")
        else:
            print_header()
            redirect_page()
            print("Username already existed, redirecting to index in 3 seconds")
            print("<a href='index.py'>Home</a>")
            # Save (commit) the changes
        conn.commit()
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()
    else:
        print_header()
        redirect_page()
        print("password not the same as confirm password, redirecting to index in 3 seconds")
        print("<a href='index.py'>Home</a>")
