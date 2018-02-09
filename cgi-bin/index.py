#!/usr/bin/env python3
import os
import sqlite3
from http import cookies

from cgi_helper import *

print_header()
with open('cgi-bin/' + str(os.path.basename(__file__)).split('.')[0] + ".html", 'r') as myfile:
    data = myfile.read()

user, have_session = get_current_user()
if not have_session:
    data = data.format("Visitor", "login.py", "Login", "<a href='register.py'>Register</a>")
else:
    if user:
        username = user['name']
        data = data.format(username, "logout_handler.py", "Logout", "")
    else:
        print("invalid session")
        exit(0)
print(data)
