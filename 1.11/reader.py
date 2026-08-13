from http.server import HTTPServer, BaseHTTPRequestHandler

log_file = "/usr/src/app/files/log.txt"
pingpong_file = "/usr/src/app/files/pingpong.txt"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            try:
                with open(log_file, "r") as f:
                    log = f.read().strip()
            except FileNotFoundError:
                log = "No log available yet"

            try:
                with open(pingpong_file, "r") as f:
                    count = f.read().strip()
            except FileNotFoundError:
                count = "0"

            response = f"{log}\nPing / Pongs: {count}\n"

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return


server = HTTPServer(("0.0.0.0", 8080), Handler)
print("Reader server started in port 8080", flush=True)
server.serve_forever()
