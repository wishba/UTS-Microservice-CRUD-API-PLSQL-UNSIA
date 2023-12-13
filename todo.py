from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import psycopg2

DB_HOST = "localhost"
DB_NAME = "todo"
DB_USER = "postgres"
DB_PASSWORD = "password"

class MyRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            connection = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        except Exception as e:
            print(f"Error connecting to database: {e}")
            self.send_response(500)
            self.end_headers()
            return

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM tasks")

        tasks = []
        for row in cursor:
            tasks.append({"id": row[0], "task_name": row[1]})

        cursor.close()
        connection.close()

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(tasks).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode()
        data = json.loads(body)

        task_name = data.get('task_name')

        try:
            connection = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        except Exception as e:
            print(f"Error connecting to database: {e}")
            self.send_response(500)
            self.end_headers()
            return

        cursor = connection.cursor()

        cursor.execute("INSERT INTO tasks (task_name) VALUES (%s)", (task_name,))
        connection.commit()

        cursor.close()
        connection.close()

        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Task added successfully"}).encode())

    def do_PUT(self):
        path = self.path.split("/")

        if len(path) >= 3 and path[2].isdigit():
            task_id = int(path[2])

            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode()
            data = json.loads(body)

            updated_task_name = data.get('task_name')

            try:
                connection = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
            except Exception as e:
                print(f"Error connecting to database: {e}")
                self.send_response(500)
                self.end_headers()
                return

            cursor = connection.cursor()

            cursor.execute("UPDATE tasks SET task_name = %s WHERE id = %s", (updated_task_name, task_id))
            connection.commit()

            cursor.close()
            connection.close()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Task updated successfully"}).encode())

    def do_DELETE(self):
        path = self.path.split("/")

        if len(path) >= 3 and path[2].isdigit():
            task_id = int(path[2])

            try:
                connection = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
            except Exception as e:
                print(f"Error connecting to database: {e}")
                self.send_response(500)
                self.end_headers()
                return

            cursor = connection.cursor()

            cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            connection.commit()

            cursor.close()
            connection.close()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Task deleted successfully"}).encode())

PORT = 8000

with HTTPServer(('', PORT), MyRequestHandler) as server:
    print(f"Server listening on port {PORT}")
    server.serve_forever()
