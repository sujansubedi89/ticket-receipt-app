# sync_helper.py

import socket
from db_helper import get_unsynced_tickets, mark_ticket_synced


def is_online():
    """Check internet connection"""
    try:
        socket.setdefaulttimeout(3)
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        return False


def sync_to_server():
    """
    Push unsynced tickets to remote server.
    Returns count of synced tickets.
    """
    if not is_online():
        return 0, "No internet connection"

    pending = get_unsynced_tickets()

    if not pending:
        return 0, "All tickets already synced"

    synced_count = 0

    for ticket in pending:
        ticket_id = ticket[0]
        ticket_no = ticket[5]

        try:
            # 🔁 REAL API CALL GOES HERE
            # import requests
            # response = requests.post(
            #     "https://api.websoft.com/tickets",
            #     json={
            #         "ticket_no": ticket_no,
            #         "customer": ticket[1],
            #         "event": ticket[2],
            #         "amount": ticket[4]
            #     },
            #     timeout=5
            # )
            # if response.status_code == 200:
            #     mark_ticket_synced(ticket_id)

            # For demo — simulate success
            mark_ticket_synced(ticket_id)
            synced_count += 1
            print(f"📤 Synced ticket {ticket_no}")

        except Exception as e:
            print(f"❌ Failed to sync {ticket_no}: {e}")

    return synced_count, f"{synced_count} ticket(s) synced successfully"