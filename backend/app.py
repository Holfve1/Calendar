import os

from lib.app import create_app
from lib.database_connection import DatabaseConnection

connection = DatabaseConnection()
connection.connect()

app = create_app(connection)

if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    is_network_exposed = host != "127.0.0.1"
    app.run(host=host, debug=not is_network_exposed, port=int(os.environ.get("PORT", 5001)))
