import sqlite3
import io


conn = sqlite3.connect(bytes(database))

conn.close()