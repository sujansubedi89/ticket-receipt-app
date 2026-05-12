# utils.py

import random
import string
from datetime import datetime


def generate_ticket_no():
    """Generate unique ticket number like TKT-20260512-A3X9"""
    date_part = datetime.now().strftime("%Y%m%d")
    rand_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"TKT-{date_part}-{rand_part}"


def format_currency(amount):
    """Format number as currency"""
    return f"${amount:,.2f}"