from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

url_map = {
    '/thelife': 'thelifeisrealgood.html',
    '/sonio': 'about.html',
    '/contact': 'contact.html',
}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/shorten':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed_data = parse_qs(post_data)
            requested_path = parsed_data.get('url', [''])[0]
            if requested_path in url_map:
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open('about.html', 'rb') as f:
                    self.wfile.write(f.read())
                return
            else:
                # If path isn't in our map, go back home or show error
                self.send_response(303) # "See Other"
                self.send_header('Location', '/')
                self.end_headers()
                self.send_response(200)

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as f:
                self.wfile.write(f.read())
            return
        
        if self.path in url_map:
            self.send_response(301)
            self.send_header('Location', url_map[self.path])
            self.end_headers()
            return
        #fallback response
        self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"404 Not Found")

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello, Http!")

server = HTTPServer(('localhost', 8080), Handler)
server.serve_forever()