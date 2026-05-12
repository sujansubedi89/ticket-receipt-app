# 🎫 Ticket Receipt System
### Offline-First Desktop App | Built with Python

> Generate tickets and receipts offline. Auto-syncs to server when internet is available.
> Built for rural areas with low or no internet connectivity.

---

## 📸 Features

- ✅ Generate tickets with unique ticket numbers (e.g. `TKT-20260512-X3K9`)
- ✅ Auto-generate professional PDF tickets
- ✅ Works fully **offline** — saves to local SQLite database
- ✅ Detects internet every 5 seconds automatically
- ✅ **Auto-syncs** unsynced tickets when internet is restored
- ✅ View all tickets in a clean table with sync status
- ✅ Open PDF output folder in one click
- ✅ Packaged as `.exe` — no Python needed on client machine

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Core language |
| Tkinter + ttk | Desktop GUI |
| SQLite3 | Offline local database |
| fpdf2 | PDF ticket generation |
| Socket | Internet connection detection |
| PyInstaller | Package as standalone .exe |

---

## 📁 Project Structure

```
ticket-receipt-app/
│
├── main.py              # Entry point — runs the GUI app
├── db_helper.py         # All SQLite database operations
├── sync_helper.py       # Internet detection + server sync
├── pdf_generator.py     # PDF ticket generation (fpdf2)
├── utils.py             # Ticket number generator + currency formatter
│
├── tickets.db           # Auto-created SQLite database (offline storage)
├── output/              # Auto-created folder — PDF tickets saved here
│
├── dist/
│   └── TicketSystem.exe # Compiled executable (after PyInstaller build)
│
└── README.md            # This file
```

---

## ⚙️ Installation & Setup

### 1. Clone or Download the Project

```bash
git clone https://github.com/sujansubedi89/ticket-receipt-app.git
cd ticket-receipt-app
```

### 2. Install Dependencies

```bash
pip install fpdf2
```

> All other libraries (tkinter, sqlite3, socket) are built into Python.

### 3. Run the App

```bash
python main.py
```

---

## 📦 Build Standalone .exe (For Rural Deployment)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "TicketSystem" main.py
```

Find your executable at:
```
dist/TicketSystem.exe
```

Copy only `TicketSystem.exe` to the client computer via USB.
No Python installation required on the client machine.

---

## 🗄️ Database Schema

```sql
CREATE TABLE tickets (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    customer    TEXT    NOT NULL,
    event       TEXT    NOT NULL,
    seat        TEXT    NOT NULL,
    amount      REAL    NOT NULL,
    ticket_no   TEXT    UNIQUE NOT NULL,
    synced      INTEGER DEFAULT 0,
    created_at  TEXT    DEFAULT CURRENT_TIMESTAMP
);
```

| Column | Description |
|---|---|
| `ticket_no` | Unique ID like `TKT-20260512-X3K9` |
| `synced` | `0` = not synced, `1` = synced to server |
| `created_at` | Auto-set timestamp |

---

## 🔄 Offline-First Architecture

```
User generates ticket
        │
        ▼
Save to SQLite (always — online or offline)
        │
        ▼
Generate PDF ticket locally
        │
        ▼
Check internet every 5 seconds
        │
   ┌────┴────┐
Offline    Online
        │
        ▼
Push unsynced tickets to server API
        │
        ▼
Mark tickets as synced in SQLite
```

---

## 🌐 API Integration (Server Sync)

To connect to a real backend, open `sync_helper.py` and uncomment:

```python
import requests

response = requests.post(
    "https://your-api.com/tickets",
    json={
        "ticket_no": ticket_no,
        "customer":  customer,
        "event":     event,
        "amount":    amount
    },
    timeout=5
)
```

Replace `https://your-api.com/tickets` with your actual server endpoint.

---

## 🔒 Security & Privacy

- Source code is compiled into `.exe` — not visible to end users
- Database stays local on the client machine
- Only ticket data (no passwords or sensitive info) is synced to server

---

## 🗺️ Roadmap — Planned Features

- [ ] User login with Admin / Cashier roles
- [ ] Search and filter tickets by customer, date, event
- [ ] Direct print support (send PDF to printer)
- [ ] Sales dashboard with daily revenue charts
- [ ] QR code on each ticket for gate scanning
- [ ] Background auto-sync thread (no manual button needed)
- [ ] Multi-language support for rural regions
- [ ] Database backup and restore
- [ ] Dark / Light theme toggle

---

## 👨‍💻 Author

**Sujan subedi**
Built for Websoft — Offline Ticket System Project

---

## 📄 License

This project is licensed for use by Websoft.
All rights reserved.
