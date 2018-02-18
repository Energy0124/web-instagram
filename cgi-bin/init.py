#!/usr/bin/env python3
import cgi

from cgi_helper import *


def init():
    with open('cgi-bin/' + str(os.path.basename(__file__)).split('.')[0] + ".html", 'r') as myfile:
        data = myfile.read()
    cursor = get_cursor()
    cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='users';""")
    result = cursor.fetchone()
    if result:
        user, have_session = get_current_user()
        if not have_session:
            print_header()
            print('<h1>Please login first</h1>')
            print("<a href='login.py'>Login</a>")
            return
        elif not user:
            C = get_clear_cookie()
            print_header(C)
            # data = data.format("Invalid session.")
            print('<h1>Please login first</h1>')
            print("<a href='login.py'>Login</a>")
            return
        elif user and user["name"] != "Admin":
            print_header()
            print('<h1>Only Admin can access this system</h1>')
            print("<a href='index.py'>Home</a>")
            return
        else:
            form = cgi.FieldStorage()
            if 'go' not in form:
                print_header()
                print('<h1>Do not visit this page directly</h1>')
                return
            else:
                go = form['go'].value
            if go != "1":
                print_header()
                print('<h1>Do not visit this page directly</h1>')
                return
            else:
                clear_images_db()
                delete_all_images()
                data = data.format("Initialization completed", "<!--", "-->")

    else:
        form = cgi.FieldStorage()
        if 'go' not in form:
            print_header()
            print('<h1>Do not visit this page directly</h1>')
            return
        else:
            go = form['go'].value
        if go != "1":
            print_header()
            print('<h1>Do not visit this page directly</h1>')
            return
        else:
            data = data.format("Admin account setup", " ", " ")
    print_header()
    print(data)
    close_db(cursor.connection)


init()
