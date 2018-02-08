from http.server import HTTPServer, CGIHTTPRequestHandler
import webbrowser


class Handler(CGIHTTPRequestHandler):
    cgi_directories = ["/cgi-bin"]

    def do_HEAD(self):
        super().do_HEAD()

    def do_POST(self):
        super().do_POST()

    def do_GET(self):
        super().do_GET()


PORT = 8080

url = 'http://localhost:{0}/{1}'.format(PORT, "cgi-bin/test.py")
webbrowser.open_new_tab(url)

httpd = HTTPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()
