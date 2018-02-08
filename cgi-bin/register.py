import cgi
import cgitb
import sqlite3

cgitb.enable()

print("Content-Type: text/html")  # HTML is following
print()  # blank line, end of headers

form = cgi.FieldStorage()

def create_user(username, password):
    import hashlib, uuid
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
    session_id = uuid.uuid4().hex
    cursor.execute("INSERT INTO users(name, password_hash, salt, session_id, session_expiry) VALUES (?,?,?,?,?)",
                   (username, hashed_password, salt, session_id, None))
    # Save (commit) the changes
    conn.commit()
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()


if "username" not in form or "password" not in form or "confirm_password" not in form:
    print("<H1>Error</H1>")
    print("Please fill in the username, password and confirm_password fields.")
else:
    username = form["username"].value
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
            create_user(username, password)
            print("Successfully registered")
        else:
            print("Username already existed")

    else:
        print("password not the same as confirm password")


