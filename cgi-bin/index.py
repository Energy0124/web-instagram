#!/usr/bin/env python3
import cgi
import cgitb
from math import ceil

from cgi_helper import *


def generate_image_list_and_pagination(images_rows):
    images_count = len(images_rows)
    images_rows = images_rows[8 * (page - 1):8 * (page)]
    images_list = ""
    images_list += "<div>"
    for image in images_rows:
        images_list += "<a href='" + image["path"] + "'><img src='" + image["path"] + "' class='thumb'></a>"
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
print_header()
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
    images = get_images()
    images_html, bar_html = generate_image_list_and_pagination(images)
    data = data.format("Visitor", "login.py", "Login", "<a href='register.py'>Register</a>", images_html, bar_html)
else:
    if user:
        username = user['name']
        uid = user['id']
        images = get_images(uid)
        images_html, bar_html = generate_image_list_and_pagination(images)
        data = data.format(username, "logout_handler.py", "Logout", "", images_html, bar_html)
    else:
        print("invalid session")
        exit(0)
print(data)
