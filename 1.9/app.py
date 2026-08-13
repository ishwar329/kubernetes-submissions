from http.server import HTTPServer, BaseHTTPRequestHandler

counter = 0


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global counter

        if self.path == "/pingpong":
            response = f"pong {counter}\n"
            counter += 1

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
