#!/usr/bin/env python3
from cgi_helper import print_header

print_header()
with open('cgi-bin/login.html', 'r') as myfile:
    data = myfile.read()
    print(data)
