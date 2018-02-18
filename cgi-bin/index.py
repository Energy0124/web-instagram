#!/usr/bin/env python3
import cgi
import cgitb
import html
from math import ceil

from cgi_helper import *

upload_form = """
<form action="/cgi-bin/upload.py" method="POST" enctype="multipart/form-data">
    File: <input name="file" type="file" accept="image/gif, image/jpeg, image/png">
    <input type="radio" name="private" value="1"> Private
    <input type="radio" name="private" value="0" checked> Public
    <input name="submit" type="submit">
</form>
"""


def generate_image_list_and_pagination(images_rows):
    images_count = len(images_rows)
    images_rows = images_rows[8 * (page - 1):8 * (page)]
    images_list = ""
    images_list += "<div>"
    for count, image in enumerate(images_rows, start=1):
        images_list += "<a href='" + image["path"] + "'><img src='" + image["path"] + "' class='thumb'></a>"
        if count % 4 == 0:
            images_list += "<br>"

    images_list += "</div>"
    previous_page = clamp(page - 1, 1, ceil(images_count / 8))
    next_page = clamp(page + 1, 1, ceil(images_count / 8))
    max_page = ceil(images_count / 8)
    pagination_bar = """
    <form action="/cgi-bin/index.py" method="GET">
    """
    if page != 1:
        pagination_bar += """ <a class="btn" href="/cgi-bin/index.py?page=""" + str(previous_page) + """\">
              Previous</a> """
    if page != max_page:
        pagination_bar += """<a class="btn" href="/cgi-bin/index.py?page=""" + str(next_page) + """\">
              Next</a>"""
    pagination_bar += """<label>Current Page:
            <input type="number" min="1" max=\"""" + str(max_page) + """\"  value=\"""" + str(page) + """\" name="page">
        </label>
        <input type="submit" value="Go">
    </form>
    """

    return images_list, pagination_bar


cgitb.enable()

cursor = get_cursor()
cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='users';""")
result = cursor.fetchone()
if not result:
    print_header()
    print("<h1>Please initialize system first</h1><a href='/init.html'>Init</a>")
    exit(0)

with open('cgi-bin/' + str(os.path.basename(__file__)).split('.')[0] + ".html", 'r') as myfile:
    data = myfile.read()
images_html = ""
bar_html = ""
form = cgi.FieldStorage()
if not 'page' in form:
    page = 1
else:
    page = int(form["page"].value)

user, have_session = get_current_user()

if not have_session:
    print_header()
    images = get_images()
    images_html, bar_html = generate_image_list_and_pagination(images)
    data = data.format("Visitor", "login.py", "Login", "<a href='register.py'>Register</a>", images_html, bar_html, "")
else:
    if user:
        print_header()
        username = user['name']
        username = html.escape(username)
        uid = user['id']
        images = get_images(uid)
        images_html, bar_html = generate_image_list_and_pagination(images)
        data = data.format(username, "logout_handler.py", "Logout", "<a href='update_password.py'>Change Password</a>",
                           images_html, bar_html, upload_form)
    else:
        # invalid session, clear the cookie
        C = get_clear_cookie()
        print_header(C)
        images = get_images()
        images_html, bar_html = generate_image_list_and_pagination(images)
        data = data.format("Visitor", "login.py", "Login", "<a href='register.py'>Register</a>", images_html, bar_html,
                           "")
print(data)
