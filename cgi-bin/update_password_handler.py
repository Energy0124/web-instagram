#!/usr/bin/env python3
import cgi
import cgitb

from cgi_helper import *

cgitb.enable()

form = cgi.FieldStorage()

if "password" not in form or "new_password" not in form or "confirm_new_password" not in form:
    print_header()
    redirect_page()
    print("<H1>Error</H1>")
    print("Please fill in the username and password  fields, redirecting to index in 3 seconds")
    print("<a href='index.py'>Home</a>")
else:
    http_cookie = os.environ["HTTP_COOKIE"]
    C = cookies.SimpleCookie()
    C.load(http_cookie)
    if "session_id" not in C:
        print_header()
        redirect_page()
        print("<H1>Error</H1>")
        print("Please login first, redirecting to index in 3 seconds")
        print("<a href='index.py'>Home</a>")
    else:
        session_id = C["session_id"].value
        new_password = form["new_password"].value
        password = form["password"].value
        confirm_new_password = form["confirm_new_password"].value
        conn = sqlite3.connect('web-instagram.sqlite')
        conn.row_factory = sqlite3.Row
        # prepare a cursor object using cursor() method
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE session_id=?", (session_id,))
        result = cursor.fetchone()
        if result is None:
            C = get_clear_cookie()
            print_header(C)
            redirect_page()
            print("invalid session, redirecting to index in 3 seconds")
        else:
            salt = result['salt']
            username = result['name']
            hashed_password = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
            password_hash = result['password_hash']

            if hashed_password == password_hash:
                if new_password == confirm_new_password:
                    hashed_password = hashlib.sha512((new_password + salt).encode('utf-8')).hexdigest()
                    cursor.execute("UPDATE users SET password_hash = ? WHERE name = ?", (hashed_password, username,))

                    print_header()
                    redirect_page()
                    print("Successfully update password, redirecting to index in 3 seconds")
                    print("<a href='index.py'>Home</a>")

                else:
                    print_header()
                    redirect_page()
                    print("incorrect confirm password, redirecting to index in 3 seconds")
                    print("<a href='index.py'>Home</a>")
            else:
                print_header()
                redirect_page()
                print("incorrect password, redirecting to index in 3 seconds")
                print("<a href='index.py'>Home</a>")

        conn.commit()
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()
