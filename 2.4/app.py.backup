import os
import time
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

port = int(os.getenv("PORT", "8080"))

IMAGE_URL = "https://picsum.photos/1200"
IMAGE_PATH = os.getenv("IMAGE_PATH", "files/image.jpg")
CACHE_TIME = 600  # 10 minutes


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
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

            todos = [
                "Learn Kubernetes basics",
                "Deploy application to cluster",
                "Configure persistent volumes",
            ]

            todo_items = "".join(
                f"<li>{todo}</li>" for todo in todos
            )

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

                <div>
                    <input
                        type="text"
                        maxlength="140"
                        placeholder="Enter a new todo (max 140 characters)"
                    >
                    <button type="button">Send</button>
                </div>

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

    def log_message(self, format, *args):
        return


server = HTTPServer(("0.0.0.0", port), Handler)

print(f"Server started in port {port}", flush=True)

server.serve_forever()
