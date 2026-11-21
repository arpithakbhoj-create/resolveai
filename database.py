
import sqlite3
from pathlib import Path


# Database file location
import os

DATABASE_PATH = Path(
    os.getenv(
        "DATABASE_PATH",
        str(Path(__file__).resolve().parent / "resolveai.db")
    )
)

DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

# Create a connection to SQLite
def get_db_connection():
    connection = sqlite3.connect(DATABASE_PATH)

    # Allow accessing database columns by name
    connection.row_factory = sqlite3.Row

    return connection


# Create the incidents table
def initialize_database():
    connection = get_db_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Open',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
                           
        """)

        # Check existing database columns
        columns = {
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(incidents)"
            ).fetchall()
        }

        # Add resolution notes if missing
        if "resolution_notes" not in columns:
            connection.execute(
                "ALTER TABLE incidents ADD COLUMN resolution_notes TEXT"
            )

        # Add resolution timestamp if missing
        if "resolved_at" not in columns:
            connection.execute(
                "ALTER TABLE incidents ADD COLUMN resolved_at TEXT"
            )
        
        # Create incident history table
        connection.execute("""
            CREATE TABLE IF NOT EXISTS incident_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_id INTEGER NOT NULL,
                field_name TEXT NOT NULL,
                old_value TEXT,
                new_value TEXT,
                changed_at TEXT NOT NULL,
                FOREIGN KEY (incident_id)
                    REFERENCES incidents(id)
            )
        """)


        connection.commit()

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()
    print("ResolveAI database initialized successfully")
