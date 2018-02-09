#!/usr/bin/env python3
import cgi
import cgitb
import os
import sqlite3
from http import cookies

from cgi_helper import *

cgitb.enable()
UPLOAD_DIR = './upload'
print_header()
with open('cgi-bin/' + str(os.path.basename(__file__)).split('.')[0] + ".html", 'r') as myfile:
    data = myfile.read()

user, have_session = get_current_user()
if not have_session:
    data = data.format("Please login first")
else:
    if user:
        username = user["name"]
        data = data.format("Welcome, " + username)
    else:
        data = data.format("Invalid session.")

form = cgi.FieldStorage()
if not 'file' in form:
    print('<h1>Not found parameter: file</h1>')

form_file = form['file']
if not form_file.file:
    print('<h1>Not found parameter: file</h1>')

if not form_file.filename:
    print('<h1>Not found parameter: file</h1>')

uploaded_file_path = os.path.join(UPLOAD_DIR, get_uuid() + os.path.splitext(form_file.filename)[1])
with open(uploaded_file_path, 'wb') as fout:
    while True:
        chunk = form_file.file.read(100000)
        if not chunk:
            break
        fout.write(chunk)
print(data)
