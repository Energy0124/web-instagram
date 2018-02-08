import sqlite3
from http import cookies

import os

from cgi_helper import print_header

print_header()
with open('cgi-bin/index.html', 'r') as myfile:
    data = myfile.read()

http_cookie = os.environ["HTTP_COOKIE"]
C = cookies.SimpleCookie()
C.load(http_cookie)
if "session_id" not in C:
    data = data.format("Visitor", "login.py", "Login")

else:
    session_id = C["session_id"].value
    conn = sqlite3.connect('web-instagram.sqlite')
    conn.row_factory = sqlite3.Row
    # prepare a cursor object using cursor() method
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE session_id=?", (session_id,))
    result = cursor.fetchone()
    if result == None:
        print_header()
        print("invalid session")
    else:
        username = result['name']
        data = data.format(username, "logout_handler.py", "Logout")
print(data)
