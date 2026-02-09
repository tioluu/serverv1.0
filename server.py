from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import os
from dotenv import load_dotenv
load_dotenv()

import requests


class Handler(BaseHTTPRequestHandler):
    def _set_security_headers(self):
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self' https://api.shrtco.de;")
        # self.send_header('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-XSS-Protection', '1; mode=block')
        
    def _send_json(self, status_code, payload):
        body = payload.encode('utf-8') if isinstance(payload, str) else payload
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self._set_security_headers()
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            content_length = os.path.getsize('src/index.html')
            self.send_header('Content-Length', str(content_length))
            self._set_security_headers()
            self.end_headers()
            with open('src/index.html', 'rb') as f:
                self.wfile.write(f.read())
            return
        
        if self.path == '/style.css':
            self.send_response(200)
            self.send_header('Content-type', 'text/css; charset=utf-8')
            self._set_security_headers()
            self.end_headers()
            with open('src/style.css', 'rb') as f:
                self.wfile.write(f.read())
            return
        
        if self.path == '/script.js':
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript; charset=utf-8')
            self._set_security_headers()
            self.end_headers()
            with open('src/script.js', 'rb') as f:
                self.wfile.write(f.read())
            return
        self.send_error(404)

    def do_POST(self):
        if self.path != '/shorten':
            self.send_error(404)
            return

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        parsed_data = parse_qs(body)

        long_url = parsed_data.get('url', [''])[0].strip()
        parsed = urlparse(long_url)
        if not long_url or parsed.scheme not in ('http', 'https') or not parsed.netloc:
            self._send_json(
                400,
                b'{"error":"invalid_url","message":"Please provide a valid URL starting with http:// or https://"}'
            )
            return

        url = "https://api.shrtco.de/v2/shorten"

        payload = {
            "url": long_url,
            "max-clicks": "10",
            "block-bots": "false"
        }
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {os.getenv('SPOO_API_KEY')}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        try:
            response = requests.post("https://spoo.me/", data=payload, headers=headers, timeout=10)
            self.send_response(response.status_code)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self._set_security_headers()
            self.end_headers()
            self.wfile.write(response.content)
        except requests.RequestException:
            self._send_json(
                502,
                b'{"error":"upstream_unavailable","message":"Shortener service unavailable. Please try again."}'
            )
        # print(response.text)


server = HTTPServer(('localhost', 8080), Handler)
server.serve_forever()
