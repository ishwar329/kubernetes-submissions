from http.server import HTTPServer, BaseHTTPRequestHandler
import os

file_path = "/usr/src/app/files/pingpong.txt"


def get_count():
    if not os.path.exists(file_path):
        return 0

    with open(file_path, "r") as f:
        content = f.read().strip()

    return int(content) if content else 0


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/pingpong":
            count = get_count()

            response = f"pong {count}\n"

            with open(file_path, "w") as f:
                f.write(str(count + 1))

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return


os.makedirs("/usr/src/app/files", exist_ok=True)

server = HTTPServer(("0.0.0.0", 8080), Handler)
print("Ping-pong server started in port 8080", flush=True)
server.serve_forever()
