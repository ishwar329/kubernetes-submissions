import os
from http.server import HTTPServer, BaseHTTPRequestHandler

port = int(os.getenv("PORT", "8080"))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Todo app")

server = HTTPServer(("0.0.0.0", port), Handler)

print(f"Server started in port {port}", flush=True)

server.serve_forever()
