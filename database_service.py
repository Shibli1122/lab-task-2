"""
Database Tier - Python + PostgreSQL
Manages all portfolio data persistence

WHY POSTGRESQL?
--------------
Unlike SQLite (which is just a file), PostgreSQL is a full database SERVER.
It runs as a separate service, handles multiple connections at once,
and is used in real production applications.

HOW IT WORKS:
------------
1. Python connects to PostgreSQL using the 'psycopg2' library
2. We create tables (projects, skills, messages) if they don't exist
3. The Node.js backend calls this Python script to read/write data
4. Data is stored permanently in PostgreSQL, not in a file
"""

import psycopg2
import psycopg2.extras
import json
import sys
from datetime import datetime

# ─── DATABASE CONNECTION CONFIG ───────────────────────────────────────────────
# Change these values to match your PostgreSQL setup
DB_CONFIG = {
    "host":     "localhost",       # Where PostgreSQL is running
    "port":     5432,              # Default PostgreSQL port
    "database": "portfolio_db",    # The database name we created
    "user":     "portfolio_user",  # PostgreSQL username
    "password": "portfolio_pass",  # PostgreSQL password
}

def get_connection():
    """
    Creates and returns a connection to PostgreSQL.
    Think of this like 'opening a phone call' to the database.
    """
    conn = psycopg2.connect(**DB_CONFIG)
    return conn


def init_db():
    """
    Creates all tables and fills them with sample data.
    Run this ONCE when setting up for the first time.

    Tables created:
    - projects  : stores portfolio project info
    - skills    : stores developer skills and levels
    - messages  : stores contact form submissions
    """
    conn = get_connection()
    cursor = conn.cursor()

    # ── CREATE TABLES ──────────────────────────────────────────────────────────

    # Projects table
    # SERIAL = auto-incrementing ID (1, 2, 3...)
    # TEXT   = any length string
    # NOT NULL = this field is required
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id          SERIAL PRIMARY KEY,
            title       TEXT NOT NULL,
            description TEXT,
            tech_stack  TEXT,
            image_url   TEXT,
            github_url  TEXT,
            live_url    TEXT,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Skills table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id       SERIAL PRIMARY KEY,
            name     TEXT NOT NULL,
            category TEXT,
            level    INTEGER DEFAULT 80
        )
    """)

    # Contact messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id      SERIAL PRIMARY KEY,
            name    TEXT NOT NULL,
            email   TEXT NOT NULL,
            message TEXT NOT NULL,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ── SEED SAMPLE DATA ───────────────────────────────────────────────────────
    # Only insert if tables are empty (avoid duplicates on re-run)

    cursor.execute("SELECT COUNT(*) FROM projects")
    if cursor.fetchone()[0] == 0:
        projects = [
            ("E-Commerce Platform",  "Full-stack shopping app with cart, auth, and payments.", '["React","Node.js","PostgreSQL"]', "", "https://github.com", "https://example.com"),
            ("AI Chat Dashboard",    "Real-time dashboard for monitoring AI conversations.",   '["React","Python","WebSockets"]',  "", "https://github.com", "https://example.com"),
            ("Portfolio CMS",        "A headless CMS built for developers.",                  '["Next.js","PostgreSQL","REST API"]',"", "https://github.com", "https://example.com"),
            ("Weather Analytics",    "Data visualization for historical weather patterns.",    '["D3.js","Flask","PostgreSQL"]',    "", "https://github.com", "https://example.com"),
        ]
        cursor.executemany(
            "INSERT INTO projects (title, description, tech_stack, image_url, github_url, live_url) VALUES (%s,%s,%s,%s,%s,%s)",
            projects
        )

    cursor.execute("SELECT COUNT(*) FROM skills")
    if cursor.fetchone()[0] == 0:
        skills = [
            ("React",      "Frontend", 90),
            ("Node.js",    "Backend",  85),
            ("Python",     "Backend",  88),
            ("TypeScript", "Frontend", 82),
            ("PostgreSQL", "Database", 78),
            ("Docker",     "DevOps",   70),
            ("REST APIs",  "Backend",  92),
            ("Git",        "DevOps",   88),
        ]
        cursor.executemany(
            "INSERT INTO skills (name, category, level) VALUES (%s,%s,%s)",
            skills
        )

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ PostgreSQL database initialized successfully.")


def get_all_projects():
    """Fetch all projects from PostgreSQL and return as a list of dicts."""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM projects ORDER BY created_at DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [dict(r) for r in rows]


def get_all_skills():
    """Fetch all skills from PostgreSQL, ordered by category and level."""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM skills ORDER BY category, level DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [dict(r) for r in rows]


def save_message(name, email, message):
    """Save a contact form message into the messages table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)",
        (name, email, message)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"status": "saved", "timestamp": datetime.now().isoformat()}


# ── RUN DIRECTLY TO INITIALIZE ─────────────────────────────────────────────────
if __name__ == "__main__":
    print("Connecting to PostgreSQL...")
    init_db()
    print("\n--- Projects in DB ---")
    print(json.dumps(get_all_projects(), indent=2, default=str))
    print("\n--- Skills in DB ---")
    print(json.dumps(get_all_skills(), indent=2, default=str))
