#!/usr/bin/env python3
import cgitb

from cgi_helper import *

cgitb.enable()

http_cookie = os.environ["HTTP_COOKIE"]
C = cookies.SimpleCookie()
C.load(http_cookie)

if "session_id" not in C:
    print_header()
    print("<H1>Error</H1>")
    print("You are already logged out.")
else:
    session_id = C["session_id"].value
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
        username = result['name']
        cursor.execute("UPDATE users SET session_id = ? WHERE name = ?", (None, username,))
        C = get_clear_cookie()
        print_header(C)
        redirect_page()
        print("logout successfully, redirecting to index in 3 seconds")

    conn.commit()
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
