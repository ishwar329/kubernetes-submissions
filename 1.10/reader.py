from http.server import HTTPServer, BaseHTTPRequestHandler

file_path = "/usr/src/app/files/log.txt"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            try:
                with open(file_path, "r") as f:
                    content = f.read()
            except FileNotFoundError:
                content = "No log available yet\n"

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(content.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return


server = HTTPServer(("0.0.0.0", 8080), Handler)

print("Reader server started in port 8080", flush=True)

server.serve_forever()
