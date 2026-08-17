from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen
import os

log_file = "/usr/src/app/files/log.txt"
information_file = "/usr/src/app/config/information.txt"
pingpong_url = "http://ping-pong-svc:8080/pingpong"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            try:
                with open(information_file, "r") as f:
                    file_content = f.read().strip()
            except FileNotFoundError:
                file_content = "File not found"

            message = os.getenv("MESSAGE", "MESSAGE not set")

            try:
                with open(log_file, "r") as f:
                    log = f.read().strip()
            except FileNotFoundError:
                log = "No log available yet"

            try:
                with urlopen(pingpong_url, timeout=5) as response:
                    pong = response.read().decode().strip()
            except Exception as e:
                pong = f"Error: {e}"

            response = (
                f"file content: {file_content}\n"
                f"env variable: MESSAGE={message}\n"
                f"{log}\n"
                f"Ping / Pongs: {pong}\n"
            )

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
