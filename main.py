from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

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

        cursor.execute("""
                       SELECT id, 
                       pgp_sym_decrypt(user_name, %s) as user_name, 
                       pgp_sym_decrypt(user_password, %s) as user_name
                       FROM data_user
                       """, (ADMIN_PASSWORD, ADMIN_PASSWORD))

        user = []
        for row in cursor:
            user.append({"id": row[0], "user_name": row[1], "user_password": row[2]})

        cursor.close()
        connection.close()

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(user).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode()
        data = json.loads(body)

        user_name = data.get('user_name')
        user_password = data.get('user_password')

        try:
            connection = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        except Exception as e:
            print(f"Error connecting to database: {e}")
            self.send_response(500)
            self.end_headers()
            return

        cursor = connection.cursor()

        cursor.execute("""
                       INSERT INTO data_user (user_name, user_password) 
                       VALUES (encrypt_data(%s, %s), encrypt_data(%s, %s))
                       """, (user_name, ADMIN_PASSWORD, user_password, ADMIN_PASSWORD))
        connection.commit()

        cursor.close()
        connection.close()

        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"message": "user added successfully"}).encode())

    def do_PUT(self):
        path = self.path.split("/")

        if len(path) >= 3 and path[2].isdigit():
            user_id = int(path[2])

            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode()
            data = json.loads(body)

            updated_user_name = data.get('user_name')
            updated_user_password = data.get('user_password')

            try:
                connection = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
            except Exception as e:
                print(f"Error connecting to database: {e}")
                self.send_response(500)
                self.end_headers()
                return

            cursor = connection.cursor()

            cursor.execute("""
                           UPDATE data_user 
                           SET 
                           user_name = encrypt_data(%s, %s) ,
                           user_password = encrypt_data(%s, %s)
                           WHERE id = %s
                           """, (updated_user_name, ADMIN_PASSWORD, updated_user_password, ADMIN_PASSWORD, user_id))
            connection.commit()

            cursor.close()
            connection.close()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "user updated successfully"}).encode())

    def do_DELETE(self):
        path = self.path.split("/")

        if len(path) >= 3 and path[2].isdigit():
            user_id = int(path[2])

            try:
                connection = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
            except Exception as e:
                print(f"Error connecting to database: {e}")
                self.send_response(500)
                self.end_headers()
                return

            cursor = connection.cursor()

            cursor.execute("""
                           DELETE FROM data_user WHERE id = %s
                           """, (user_id,))
            connection.commit()

            cursor.close()
            connection.close()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "user deleted successfully"}).encode())

PORT = 8000

with HTTPServer(('', PORT), MyRequestHandler) as server:
    print(f"Server listening on port {PORT}")
    server.serve_forever()
