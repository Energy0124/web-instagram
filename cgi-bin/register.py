from cgi_helper import print_header

print_header()
with open('cgi-bin/register.html', 'r') as myfile:
    data=myfile.read()
print(data)