from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

url_map = {
    '/about': 'about.html',
    '/contact': 'contact.html',
}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/shorten':
            self.send_error(404)
            return

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode()
        parsed_data = parse_qs(post_data)

        requested_path = parsed_data.get('url', [''])[0]

        if requested_path in url_map:
            self.send_response(303)  # POST → GET redirect
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', requested_path)
            self.end_headers()
        else:
            self.send_error(404, "URL not found")


    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as f:
                self.wfile.write(f.read())
            return
        
        if self.path in url_map:
            file = url_map[self.path]
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            with open(file, 'rb') as f:
                self.wfile.write(f.read())
            return
        
        self.send_error(404)
        
server = HTTPServer(('localhost', 8080), Handler)
server.serve_forever()