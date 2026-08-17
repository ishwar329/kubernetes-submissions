from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

todos = [
    {"id": 1, "content": "Learn Kubernetes basics"},
    {"id": 2, "content": "Deploy application to cluster"},
    {"id": 3, "content": "Configure persistent volumes"},
]


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/todos":
            response = json.dumps(todos).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/todos":
            try:
                length = int(self.headers.get("Content-Length", 0))
                data = json.loads(self.rfile.read(length))

                content = data.get("content", "").strip()

                if not content or len(content) > 140:
                    self.send_response(400)
                    self.end_headers()
                    return

                todo = {
                    "id": len(todos) + 1,
                    "content": content,
                }

                todos.append(todo)

                response = json.dumps(todo).encode()

                self.send_response(201)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(response)))
                self.end_headers()
                self.wfile.write(response)

            except Exception:
                self.send_response(400)
                self.end_headers()

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return


port = int(os.environ["PORT"])

server = HTTPServer(("0.0.0.0", port), Handler)
print(f"Todo backend started in port {port}", flush=True)
server.serve_forever()
