import os
import time
import json
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

port = int(os.environ["PORT"])

IMAGE_URL = os.getenv("IMAGE_URL")
IMAGE_PATH = os.getenv("IMAGE_PATH", "files/image.jpg")
CACHE_TIME = int(os.environ["CACHE_TIME"])
TODO_BACKEND_URL = os.getenv("TODO_BACKEND_URL")


def get_image():
    os.makedirs(os.path.dirname(IMAGE_PATH), exist_ok=True)

    if os.path.exists(IMAGE_PATH):
        age = time.time() - os.path.getmtime(IMAGE_PATH)

        if age < CACHE_TIME:
            return

    print("Downloading new image...", flush=True)

    request = urllib.request.Request(
        IMAGE_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read()

    with open(IMAGE_PATH, "wb") as f:
        f.write(data)

    print(f"Image cached: {len(data)} bytes", flush=True)


def get_todos():
    try:
        with urllib.request.urlopen(
            f"{TODO_BACKEND_URL}/todos",
            timeout=5
        ) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching todos: {e}", flush=True)
        return []


def create_todo(content):
    data = json.dumps({"content": content}).encode()

    request = urllib.request.Request(
        f"{TODO_BACKEND_URL}/todos",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=5) as response:
        return json.loads(response.read().decode())


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            todos = get_todos()

            todo_items = "".join(
                f"<li>{todo['content']}</li>"
                for todo in todos
            )

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Todo App</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        text-align: center;
                    }}

                    img {{
                        max-width: 800px;
                        width: 90%;
                    }}

                    input {{
                        width: 360px;
                        padding: 10px;
                        font-size: 16px;
                    }}

                    button {{
                        padding: 10px 20px;
                        font-size: 16px;
                    }}

                    ul {{
                        list-style: none;
                        padding: 0;
                        max-width: 600px;
                        margin: 20px auto;
                    }}

                    li {{
                        padding: 12px;
                        margin: 8px 0;
                        background: #f5f5f5;
                        border-left: 4px solid #4caf50;
                        text-align: left;
                    }}
                </style>
            </head>
            <body>
                <h1>Todo App</h1>

                <img src="/image.jpg" alt="Random image">

                <form action="/todos" method="post">
                    <input
                        type="text"
                        name="content"
                        maxlength="140"
                        required
                        placeholder="Enter a new todo (max 140 characters)"
                    >
                    <button type="submit">Send</button>
                </form>

                <h2>Todos</h2>

                <ul>
                    {todo_items}
                </ul>

                <p>DevOps with Kubernetes 2026</p>
            </body>
            </html>
            """

            self.wfile.write(html.encode())

        elif self.path == "/image.jpg":
            try:
                get_image()

                with open(IMAGE_PATH, "rb") as image:
                    data = image.read()

                self.send_response(200)
                self.send_header("Content-Type", "image/jpeg")
                self.end_headers()
                self.wfile.write(data)

            except Exception as e:
                print(f"Error downloading image: {e}", flush=True)
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Failed to load image")

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/todos":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode()

            from urllib.parse import parse_qs
            form = parse_qs(body)

            content = form.get("content", [""])[0].strip()

            if not content or len(content) > 140:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid todo")
                return

            try:
                create_todo(content)

                self.send_response(303)
                self.send_header("Location", "/")
                self.end_headers()

            except Exception as e:
                print(f"Error creating todo: {e}", flush=True)
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Failed to create todo")

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return


server = HTTPServer(("0.0.0.0", port), Handler)

print(f"Server started in port {port}", flush=True)

server.serve_forever()
