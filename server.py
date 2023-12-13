from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class MyRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Send a simple response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'message': 'Hello, world!'}).encode())

    def do_POST(self):
        # Get request body data
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode()
        data = json.loads(body)

        # Extract name from the JSON data
        name = data.get('name')

        # Create a new message
        message = f"Your name is: {name}"

        # Send the response with the new message
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'message': message}).encode())

PORT = 8000

with HTTPServer(('', PORT), MyRequestHandler) as server:
    print(f"Server listening on port {PORT}")
    server.serve_forever()
