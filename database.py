
import sqlite3
import os


class SentinelDatabase:

    def __init__(self, path="/content/sentinel/data/sentinel.db"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.path = path
        self.create_table()

    def connect(self):
        return sqlite3.connect(self.path)

    def create_table(self):
        with self.connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS incidents (
                    incident_id TEXT PRIMARY KEY,
                    event_type TEXT,
                    camera TEXT,
                    timestamp_seconds REAL,
                    frame_number INTEGER,
                    severity TEXT,
                    person_id INTEGER,
                    status TEXT
                )
            """)

    def insert(self, incident):
        with self.connect() as conn:
            conn.execute("""
                INSERT OR IGNORE INTO incidents
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                incident["Incident_ID"],
                incident["Event"],
                incident["Camera"],
                incident["Timestamp_seconds"],
                incident["Frame"],
                incident["Severity"],
                incident["Person_ID"],
                incident["Status"]
            ))

    def get_all(self):
        with self.connect() as conn:
            return conn.execute(
                "SELECT * FROM incidents ORDER BY rowid DESC"
            ).fetchall()
