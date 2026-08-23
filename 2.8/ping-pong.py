from http.server import HTTPServer, BaseHTTPRequestHandler
import os

COUNTER_FILE = "/usr/src/app/files/count.txt"


def get_count():
    try:
        with open(COUNTER_FILE, "r") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0


def save_count(count):
    os.makedirs(os.path.dirname(COUNTER_FILE), exist_ok=True)
    with open(COUNTER_FILE, "w") as f:
        f.write(str(count))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/pingpong":
            count = get_count()

            response = f"pong {count}\n"

            save_count(count + 1)

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
print("Ping-pong server started in port 8080", flush=True)
server.serve_forever()
