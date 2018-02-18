#!/usr/bin/env python3
import cgi
import cgitb

from cgi_helper import *

cgitb.enable()

form = cgi.FieldStorage()

if "password" not in form or "confirm_password" not in form:
    print_header()
    print("""
           <meta http-equiv="refresh" content="3;url=init.py?go=1">
           """)
    print("<H1>Error</H1>")
    print("Please fill in the password and confirm_password fields, redirecting to init.py  in 3 seconds")
else:

    username = "Admin"
    password = form["password"].value
    confirm_password = form["confirm_password"].value
    # print("<p>username:", form["username"].value)
    # print("<p>password:", form["password"].value)
    # print("<p>confirm_password:", form["confirm_password"].value)
    if confirm_password == password:
        reset_all_tables()
        delete_all_images()

        conn = sqlite3.connect('web-instagram.sqlite')
        # prepare a cursor object using cursor() method
        cursor = conn.cursor()

        session_id = create_user(cursor, username, password)
        C = cookies.SimpleCookie()
        C["session_id"] = session_id
        C["session_id"]["path"] = "/"
        C["session_id"]["max-age"] = 2147483647
        print_header(C)
        print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Initialization</title>
    <link rel="stylesheet" type="text/css" href="../style.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
          integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

</head>
<body>
<h1>Initialization</h1>
<p>Successfully setup Admin account! Initialization completed.
</p><br>

<a href="index.py">Home</a>
</body>
</html>
     """)
        conn.commit()
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()

    else:
        print_header()
        print("""
               <meta http-equiv="refresh" content="3;url=init.py?go=1">
               """)
        print("<H1>Error</H1>")
        print("Please fill in the correct password and confirm_password fields, redirecting to init.py  in 3 seconds")
