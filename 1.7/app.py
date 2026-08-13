import os
import time
import uuid
import threading
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler

random_string = str(uuid.uuid4())
port = int(os.getenv("PORT", "8080"))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            timestamp = datetime.now(timezone.utc).isoformat()
            response = f"Timestamp: {timestamp}\nRandom string: {random_string}\n"

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return


def log_output():
    while True:
        timestamp = datetime.now(timezone.utc).isoformat()
        print(f"{timestamp}: {random_string}", flush=True)
        time.sleep(5)


server = HTTPServer(("0.0.0.0", port), Handler)

print(f"Server started in port {port}", flush=True)

threading.Thread(target=log_output, daemon=True).start()

server.serve_forever()
