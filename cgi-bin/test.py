#!/usr/bin/env python3
import cgi
import cgitb
import time
import os
import html

cgitb.enable()

hit_count_path = os.path.join(os.path.dirname(__file__), "noob-count.txt")

if os.path.isfile(hit_count_path):
    hit_count = int(open(hit_count_path).read())
    hit_count += 1
else:
    hit_count = 1

hit_counter_file = open(hit_count_path, 'w')
hit_counter_file.write(str(hit_count))
hit_counter_file.close()

header = "Content-type: text/html\n\n"

date_string = time.strftime('%A, %B %d, %Y at %I:%M:%S %p %Z')

html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Current date</title>
</head>
<body>
  <p>
  Date: {0}
  </p>
  <p>
  Noob count: {1}
  </p>
</body>
</html>
""".format(html.escape(date_string), html.escape(str(hit_count)))

print(header + html)
