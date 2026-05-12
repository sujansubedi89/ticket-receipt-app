# db_helper.py — ALL database logic lives here

import sqlite3

DB_NAME = "tickets.db"

def init_db():
    """Create tables if they don't exist"""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            customer    TEXT    NOT NULL,
            event       TEXT    NOT NULL,
            seat        TEXT    NOT NULL,
            amount      REAL    NOT NULL,
            ticket_no   TEXT    UNIQUE NOT NULL,
            synced      INTEGER DEFAULT 0,
            created_at  TEXT    DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Database initialized")


def save_ticket(customer, event, seat, amount, ticket_no):
    """Save a new ticket offline"""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        INSERT INTO tickets (customer, event, seat, amount, ticket_no)
        VALUES (?, ?, ?, ?, ?)
    """, (customer, event, seat, amount, ticket_no))
    conn.commit()
    conn.close()


def get_all_tickets():
    """Fetch all tickets"""
    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute(
        "SELECT * FROM tickets ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return rows


def get_unsynced_tickets():
    """Fetch tickets not yet synced to server"""
    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute(
        "SELECT * FROM tickets WHERE synced=0"
    ).fetchall()
    conn.close()
    return rows


def mark_ticket_synced(ticket_id):
    """Mark a ticket as synced"""
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        "UPDATE tickets SET synced=1 WHERE id=?",
        (ticket_id,)
    )
    conn.commit()
    conn.close()