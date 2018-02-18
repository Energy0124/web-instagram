#!/usr/bin/env python3
import cgi
import cgitb

from cgi_helper import *


def save():
    cgitb.enable()
    UPLOAD_DIR = './upload'
    WEB_UPLOAD_DIR = '/upload'
    message = ""
    with open('cgi-bin/' + str(os.path.basename(__file__)).split('.')[0] + ".html", 'r') as myfile:
        data = myfile.read()

    img_html = "<img src='{0}' class='edit'>"
    user, have_session = get_current_user()
    if not have_session:
        print_header()
        print('<h1>Please login first</h1>')
        return
    elif not user:
        C = get_clear_cookie()
        print_header(C)
        # data = data.format("Invalid session.")
        print('<h1>Please login first</h1>')
        return
    else:
        print_header()

    form = cgi.FieldStorage()
    if 'image' not in form:
        print('<h1>Not found parameter: image</h1>')
        print("<a href='index.py'>Home</a>")

        return
    else:
        image_name = form['image'].value
        username = user["name"]
        image = image_exist(image_name)
        if not image and image_belongs_to(image_name, username):
            print('<h1>Invalid parameter: image not exist or not belong to you</h1>')
            return
        img_html = img_html.format(image["path"])

        refer = os.environ.get("HTTP_REFERER", "")
        if refer:
            host = refer.split('/')[2]
            part1 = refer.split('/')[0]
            host = part1 + "//" + host
        else:
            host = ""
        url = host + image["path"]
        data = data.format(message, img_html, url)
        print(data)


save()
