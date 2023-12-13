from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import psycopg2

# Database connection information
DB_HOST = "localhost"
DB_NAME = "todo"
DB_USER = "postgres"
DB_PASSWORD = "password"

class MyRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Connect to the database
        try:
            connection = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        except Exception as e:
            print(f"Error connecting to database: {e}")
            self.send_response(500)
            self.end_headers()
            return

        # Get cursor object
        cursor = connection.cursor()

        # Execute a query to retrieve all tasks
        cursor.execute("SELECT * FROM tasks")

        # Fetch results as a list of dictionaries
        tasks = []
        for row in cursor:
            tasks.append({"id": row[0], "task_name": row[1]})

        # Close cursor and connection
        cursor.close()
        connection.close()

        # Send response with the list of tasks
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(tasks).encode())

    def do_POST(self):
        # Get request body data
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode()
        data = json.loads(body)

        # Extract task name from the JSON data
        task_name = data.get('task_name')

        # Connect to the database
        try:
            connection = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        except Exception as e:
            print(f"Error connecting to database: {e}")
            self.send_response(500)
            self.end_headers()
            return

        # Get cursor object
        cursor = connection.cursor()

        # Insert the new task into the database
        cursor.execute("INSERT INTO tasks (task_name) VALUES (%s)", (task_name,))
        connection.commit()

        # Close cursor and connection
        cursor.close()
        connection.close()

        # Send a success response
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Task added successfully"}).encode())

PORT = 8000

with HTTPServer(('', PORT), MyRequestHandler) as server:
    print(f"Server listening on port {PORT}")
    server.serve_forever()
