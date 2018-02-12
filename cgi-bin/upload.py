#!/usr/bin/env python3
import cgi
import cgitb

import re
import shutil

import subprocess

from cgi_helper import *

cgitb.enable()
UPLOAD_DIR = './upload'
WEB_UPLOAD_DIR = '/upload'

with open('cgi-bin/' + str(os.path.basename(__file__)).split('.')[0] + ".html", 'r') as myfile:
    data = myfile.read()

img_html = "<img src='{0}'>"
user, have_session = get_current_user()
if not have_session:
    print_header()
    data = data.format("Please login first","")
else:
    if user:
        print_header()

    else:
        C = get_clear_cookie()
        print_header(C)
        # data = data.format("Invalid session.")
        data = data.format("Please login first","")

form = cgi.FieldStorage()
if not 'file' in form:
    print('<h1>Not found parameter: file</h1>')
else:
    form_file = form['file']
    if not form_file.file:
        print('<h1>Not found parameter: file</h1>')
    elif not form_file.filename:
        print('<h1>Not found parameter: file</h1>')
    else:
        if not 'private' in form:
            print('<h1>Not found parameter: private</h1>')
            privateImage = False
        else:
            privateImage = form['private'].value
        pattern = re.compile("^[0-9A-Za-z.\s_-]+$")
        regex_result = pattern.fullmatch(os.path.basename(form_file.filename))
        if regex_result is None:
            print('<h1>invalid filename</h1>')
        else:
            file_extension = os.path.splitext(form_file.filename)[1].lower()
            image_name = get_uuid() + file_extension
            uploaded_file_path = os.path.join(UPLOAD_DIR, image_name)
            web_file_path = WEB_UPLOAD_DIR + "/" + image_name
            with open(uploaded_file_path, 'wb') as fout:
                while True:
                    chunk = form_file.file.read(100000)
                    if not chunk:
                        break
                    fout.write(chunk)

            uid = user["id"]
            cmd_result = subprocess.run(['magick', 'identify', uploaded_file_path],
                                        stdout=subprocess.PIPE)
            cmd_result = cmd_result.stdout.decode('utf-8')
            image_type = cmd_result.split()[1]
            if image_type not in ["JPEG", "GIF", "PNG"]:
                os.remove(uploaded_file_path)
                print('<h1>invalid file type</h1>')
            elif image_type == "JPEG" and file_extension not in [".jpg", ".jpeg"]:
                os.remove(uploaded_file_path)
                print('<h1>invalid file type</h1>')
            elif image_type == "GIF" and file_extension != ".gif":
                os.remove(uploaded_file_path)
                print('<h1>invalid file type</h1>')
            elif image_type == "PNG" and file_extension != ".png":
                os.remove(uploaded_file_path)
                print('<h1>invalid file type</h1>')
            else:
                cursor = get_cursor()
                cursor.execute("""
                INSERT INTO images(name, path, uid, private) VALUES (?,?,?,?)
                """, (image_name, web_file_path, uid, privateImage))
                close_db(cursor.connection)
                username = user["name"]
                img_html= img_html.format(web_file_path)
                data = data.format("Uploaded successfully, " + username, img_html)
                print(data)
