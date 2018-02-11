#!/usr/bin/env python3
import cgitb

from cgi_helper import *

cgitb.enable()
print_header()
with open('cgi-bin/' + str(os.path.basename(__file__)).split('.')[0] + ".html", 'r') as myfile:
    data = myfile.read()
images_html = ""
user, have_session = get_current_user()
if not have_session:
    images = get_images()
    images_html += "<div>"
    for image in images:
        images_html += "<a href='" + image["path"] + "'><img src='" + image["path"] + "' class='thumb'></a>"
    images_html += "</div>"
    data = data.format("Visitor", "login.py", "Login", "<a href='register.py'>Register</a>", images_html)
else:
    if user:
        username = user['name']
        uid = user['id']
        images = get_images(uid)
        images_html += "<div>"
        for image in images:
            images_html += "<a href='" + image["path"] + "'><img src='" + image["path"] + "' class='thumb'></a>"
        images_html += "</div>"

        data = data.format(username, "logout_handler.py", "Logout", "", images_html)
    else:
        print("invalid session")
        exit(0)
print(data)
