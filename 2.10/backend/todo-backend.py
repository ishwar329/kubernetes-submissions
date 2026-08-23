from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import time
import psycopg2


DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
PORT = int(os.environ["PORT"])


def log(message):
    print(f"[TODO-REQUEST] {message}", flush=True)


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def init_db():
    for _ in range(30):
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id SERIAL PRIMARY KEY,
                    content VARCHAR(140) NOT NULL
                )
            """)

            cur.execute("SELECT COUNT(*) FROM todos")
            count = cur.fetchone()[0]

            if count == 0:
                cur.executemany(
                    "INSERT INTO todos (content) VALUES (%s)",
                    [
                        ("Learn Kubernetes basics",),
                        ("Deploy application to cluster",),
                        ("Configure persistent volumes",),
                    ],
                )

            conn.commit()
            cur.close()
            conn.close()

            print("Database initialized", flush=True)
            return

        except Exception as e:
            print(f"Waiting for database: {e}", flush=True)
            time.sleep(2)

    raise RuntimeError("Could not connect to database")


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/todos":
            log("GET /todos")

            try:
                conn = get_connection()
                cur = conn.cursor()

                cur.execute(
                    "SELECT id, content FROM todos ORDER BY id"
                )

                todos = [
                    {"id": row[0], "content": row[1]}
                    for row in cur.fetchall()
                ]

                cur.close()
                conn.close()

                response = json.dumps(todos).encode()

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(response)))
                self.end_headers()
                self.wfile.write(response)

            except Exception as e:
                log(f"GET /todos ERROR: {e}")
                self.send_response(500)
                self.end_headers()

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/todos":
            try:
                length = int(self.headers.get("Content-Length", 0))
                data = json.loads(self.rfile.read(length))

                content = data.get("content", "").strip()

                log(f"POST /todos content_length={len(content)}")

                if not content:
                    log("REJECTED: empty todo")
                    self.send_response(400)
                    self.end_headers()
                    return

                if len(content) > 140:
                    log(
                        f"REJECTED: todo exceeds 140 characters "
                        f"(length={len(content)})"
                    )
                    self.send_response(400)
                    self.end_headers()
                    return

                conn = get_connection()
                cur = conn.cursor()

                cur.execute(
                    "INSERT INTO todos (content) VALUES (%s) RETURNING id",
                    (content,),
                )

                todo_id = cur.fetchone()[0]

                conn.commit()
                cur.close()
                conn.close()

                todo = {
                    "id": todo_id,
                    "content": content,
                }

                log(f"ACCEPTED: todo id={todo_id}")

                response = json.dumps(todo).encode()

                self.send_response(201)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(response)))
                self.end_headers()
                self.wfile.write(response)

            except Exception as e:
                log(f"POST /todos ERROR: {e}")
                self.send_response(400)
                self.end_headers()

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return


init_db()

server = HTTPServer(("0.0.0.0", PORT), Handler)
print(f"Todo backend started in port {PORT}", flush=True)
server.serve_forever()
