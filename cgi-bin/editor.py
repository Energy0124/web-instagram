#!/usr/bin/env python3
import cgi
import cgitb
import re
import subprocess
from pathlib import Path

from cgi_helper import *


def editor():
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
        return
    else:
        image_name = form['image'].value
        username = user["name"]
        image = image_exist(image_name)
        if not image and image_belongs_to(image_name, username):
            print('<h1>Invalid parameter: image not exist or not belong to you</h1>')
            return
        if 'status' not in form:
            status = 0
        else:
            status = int(form["status"].value)

        if 'operation' not in form:
            operation = None
        else:
            operation = form["operation"].value
        file_extension = os.path.splitext(image_name)[1].lower()

        pre_status = status - 1
        # if pre_status < 0:
        #     pre_status = 0
        next_status = status + 1
        if status > 1:
            pre_image_name = os.path.splitext(image_name)[0] + "-" + str(pre_status) + file_extension
            next_image_name = os.path.splitext(image_name)[0] + "-" + str(status) + file_extension
        elif status == 1:
            pre_image_name = image_name
            next_image_name = os.path.splitext(image_name)[0] + "-" + str(status) + file_extension
        else:
            pre_image_name = image_name
            next_image_name = image_name

        original_file_path = os.path.join(UPLOAD_DIR, image_name)
        next_file_path = os.path.join(UPLOAD_DIR, next_image_name)
        web_file_path = WEB_UPLOAD_DIR + "/" + next_image_name

        uid = user["id"]
        cmd = None
        if status > 0:
            if operation == "border":
                cmd = ['magick', 'convert', original_file_path, '-bordercolor', 'black',
                       '-border',
                       '25',
                       next_file_path]
                cmd_result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
            elif operation == "lomo":
                cmd = ['magick', 'convert', original_file_path, '-channel', 'G',
                       '-level',
                       '33%',
                       next_file_path]
                cmd_result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')

            elif operation == "lensflare":
                uploaded_file_path = os.path.join(UPLOAD_DIR, image_name)
                temp_image_path = os.path.join(UPLOAD_DIR, os.path.splitext(image_name)[0] + "-tmp" + file_extension)
                cmd_result = subprocess.run(['magick', 'identify', uploaded_file_path],
                                            stdout=subprocess.PIPE).stdout.decode('utf-8')
                m = re.search(r"([0-9]+)x([0-9]+)\+0\+0", cmd_result)
                width = m.group(1)
                cmd = ['magick', 'convert', "./lensflare.png", '-resize', width + 'x',
                       temp_image_path]
                cmd_result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
                cmd = ['magick', 'composite', "-compose", "screen", '-gravity', 'northwest',
                       temp_image_path,
                       original_file_path,
                       next_file_path]
                cmd_result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
                os.remove(temp_image_path)
            elif operation == "blackwhite":
                uploaded_file_path = os.path.join(UPLOAD_DIR, image_name)
                temp_image_path = os.path.join(UPLOAD_DIR, os.path.splitext(image_name)[0] + "-tmp" + file_extension)
                temp2_image_path = os.path.join(UPLOAD_DIR, os.path.splitext(image_name)[0] + "-tmp2" + file_extension)
                cmd_result = subprocess.run(['magick', 'identify', uploaded_file_path],
                                            stdout=subprocess.PIPE).stdout.decode('utf-8')
                m = re.search(r"([0-9]+)x([0-9]+)\+0\+0", cmd_result)
                width = m.group(1)
                height = m.group(2)
                cmd = ['magick', 'convert', uploaded_file_path, '-type', 'grayscale',
                       temp_image_path]
                cmd_result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
                cmd = ['magick', 'convert', "./bwgrad.png", '-resize', width + 'x' + height + '!',
                       temp2_image_path]
                cmd_result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
                cmd = ['magick', 'composite', "-compose", "softlight", '-gravity', 'center',
                       temp2_image_path,
                       temp_image_path,
                       next_file_path]
                cmd_result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
                os.remove(temp_image_path)
                os.remove(temp2_image_path)
            elif operation == "blur":
                cmd = ['magick', 'convert', original_file_path, '-blur', '0.5x2',
                       next_file_path]
                cmd_result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
        if operation == "undo":
            if status < 0:
                message = "No more step to undo"
            else:
                last_image_name = os.path.splitext(image_name)[0] + "-" + str(next_status) + file_extension
                last_image_path = os.path.join(UPLOAD_DIR, last_image_name)
                if Path(last_image_path).is_file():
                    os.remove(last_image_path)
        elif operation == "discard":
            for p in Path(UPLOAD_DIR).glob(os.path.splitext(image_name)[0] + '*' + file_extension):
                p.unlink()
            cursor = get_cursor()
            cursor.execute("""
                          DELETE FROM images WHERE name=?
                           """, (image_name,))
            close_db(cursor.connection)
            print("""
                   <meta http-equiv="refresh" content="0;url=index.py">
                   """)
            return
        img_html = img_html.format(web_file_path)

        filter_html = """
              <a href='editor.py?image={}&operation=border&status={}'>Border</a>      
              <a href='editor.py?image={}&operation=lomo&status={}'>Lomo</a>      
              <a href='editor.py?image={}&operation=lensflare&status={}'>Lens Flare</a>      
              <a href='editor.py?image={}&operation=blackwhite&status={}'>Black White</a>      
              <a href='editor.py?image={}&operation=blur&status={}'>Blur</a>      
                """.format(image_name, next_status,
                           image_name, next_status,
                           image_name, next_status,
                           image_name, next_status,
                           image_name, next_status, )

        if status <= 0:
            operation_html = """
             <a href='editor.py?image={}&operation=discard&status={}'>Discard</a>      
             <a href='save.py?image={}'>Finish</a>      
                   """.format(image_name, status, image_name, )
        else:
            operation_html = """
                             <a href='editor.py?image={}&operation=undo&status={}'>Undo</a>      
                             <a href='editor.py?image={}&operation=discard&status={}'>Discard</a>     
                              <a href='save.py?image={}'>Finish</a>      

                    """.format(image_name, pre_status, image_name, status, image_name, )
        data = data.format(message, img_html, filter_html, operation_html)
        print(data)


editor()
