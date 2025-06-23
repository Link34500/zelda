import sqlite3
import io

def connect(database:bytes):
    conn = sqlite3.connect(database)
    
    conn.close()