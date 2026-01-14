import sqlite3
import json
import sys
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

class Request:
    def __init__(self, method, path, headers, body):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body

class Response:
    @staticmethod
    def json(handler, data, status=200):
        handler.send_response(status)
        handler.send_header("Content-Type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode())


class Database:
    def __init__(self, db_name="db.sqlite3"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_table(self, table, columns: dict):
        cols = ", ".join([f"{k} {v}" for k, v in columns.items()])
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({cols})")
        self.conn.commit()
        return f"Table '{table}' created successfully."

    def insert(self, table, data: dict):
        keys = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        values = tuple(data.values())
        self.cursor.execute(f"INSERT INTO {table} ({keys}) VALUES ({placeholders})", values)
        self.conn.commit()
        return {"message": f"Inserted into '{table}' successfully."}

    def fetch_all(self, table):
        self.cursor.execute(f"SELECT * FROM {table}")
        rows = self.cursor.fetchall()
        columns = [col[0] for col in self.cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
        return result


class MiniAPI:
    def __init__(self, host="localhost", port=8000):
        self.host = host
        self.port = port
        self.routes = {}
        self.db = Database()

    def route(self, path, methods=["GET"]):
        def decorator(func):
            if path not in self.routes:
                self.routes[path] = {}
            for method in methods:
                self.routes[path][method] = func
            return func
        return decorator

    def run(self):
        server = HTTPServer((self.host, self.port), self._make_handler())
        print(f"🚀 Server running at http://{self.host}:{self.port}")
        server.serve_forever()

    def _make_handler(self):
        routes = self.routes
        db = self.db

        class Handler(BaseHTTPRequestHandler):
            def handle_request(self):
                parsed = urlparse(self.path)
                path = parsed.path
                method = self.command

                if path not in routes:
                    return Response.json(self, {"error": "Not Found"}, 404)
                if method not in routes[path]:
                    return Response.json(self, {"error": "Method Not Allowed"}, 405)

                func = routes[path][method]

                length = int(self.headers.get("Content-Length", 0))
                body = json.loads(self.rfile.read(length)) if length > 0 else {}

                request = Request(method, path, self.headers, body)

                try:
                    result = func(request, db)
                    Response.json(self, result)
                except Exception as e:
                    Response.json(self, {"error": str(e)}, 500)

            def do_GET(self):
                self.handle_request()
            def do_POST(self):
                self.handle_request()
            def do_PUT(self):
                self.handle_request()

        return Handler


api = MiniAPI()

api.db.create_table(
    "users",
    {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT",
        "email": "TEXT"
    }
)

@api.route("/users", methods=["GET"])
def get_users(request, db):
    users = db.fetch_all("users")
    return {"users": users}

@api.route("/users", methods=["POST"])
def create_user(request, db):
    return db.insert("users", request.body)


def cli():
    parser = argparse.ArgumentParser(description="MiniAPI ORM CLI")
    subparsers = parser.add_subparsers(dest="command")

    ct = subparsers.add_parser("create_table")
    ct.add_argument("table")
    ct.add_argument("columns", nargs='+', help="column:type format")

    ins = subparsers.add_parser("insert")
    ins.add_argument("table")
    ins.add_argument("data", nargs='+', help="key=value format")

    fch = subparsers.add_parser("fetch")
    fch.add_argument("table")

    args = parser.parse_args()

    db = api.db

    if args.command == "create_table":
        columns = dict([col.split(":") for col in args.columns])
        print(db.create_table(args.table, columns))
    elif args.command == "insert":
        data = dict([item.split("=", 1) for item in args.data])
        print(db.insert(args.table, data))
    elif args.command == "fetch":
        result = db.fetch_all(args.table)
        print(json.dumps(result, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli()
    else:
        api.run()
