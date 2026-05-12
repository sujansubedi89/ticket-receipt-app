# main.py — run this file

import tkinter as tk
from tkinter import messagebox, ttk
import os
import subprocess
import sys

from db_helper import init_db, save_ticket, get_all_tickets
from sync_helper import is_online, sync_to_server
from pdf_generator import generate_pdf_ticket
from utils import generate_ticket_no, format_currency


class TicketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Websoft Ticket Receipt System (Demo)")
        self.root.geometry("700x580")
        self.root.configure(bg="#1a1a2e")
        self.build_ui()
        self.refresh_status()
        self.refresh_table()

    # ── UI BUILDER ─────────────────────────────────────────
    def build_ui(self):

        # Header
        tk.Label(
            self.root, text="Websoft Ticket Receipt System (Demo)",
            font=("Arial", 20, "bold"),
            bg="#1a1a2e", fg="white"
        ).pack(pady=10)

        # Status
        self.status_var = tk.StringVar()
        tk.Label(
            self.root, textvariable=self.status_var,
            font=("Arial", 10),
            bg="#1a1a2e"
        ).pack()

        # Form
        form = tk.Frame(self.root, bg="#16213e", padx=20, pady=15)
        form.pack(fill="x", padx=20, pady=10)

        fields = [
            ("Customer Name", "entry_customer"),
            ("Event Name",    "entry_event"),
            ("Seat / Section","entry_seat"),
            ("Amount ($)",    "entry_amount"),
        ]

        for i, (label, attr) in enumerate(fields):
            tk.Label(
                form, text=label,
                bg="#16213e", fg="white",
                font=("Arial", 10)
            ).grid(row=i, column=0, sticky="w", pady=4)

            entry = tk.Entry(form, width=35, font=("Arial", 10))
            entry.grid(row=i, column=1, padx=15, pady=4)
            setattr(self, attr, entry)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#1a1a2e")
        btn_frame.pack(pady=8)

        buttons = [
            (" Generate Ticket", self.on_generate, "#4CAF50"),
            ("Sync Now",        self.on_sync,     "#2196F3"),
            (" Open Output",     self.on_open_folder, "#9C27B0"),
        ]

        for text, cmd, color in buttons:
            tk.Button(
                btn_frame, text=text, command=cmd,
                bg=color, fg="white",
                font=("Arial", 10, "bold"),
                width=16, pady=4
            ).pack(side="left", padx=6)

        # Table
        tk.Label(
            self.root, text="All Tickets",
            font=("Arial", 12, "bold"),
            bg="#1a1a2e", fg="white"
        ).pack()

        cols = ("ID", "Ticket No", "Customer", "Event", "Seat", "Amount", "Synced", "Date")
        self.tree = ttk.Treeview(self.root, columns=cols, show="headings", height=10)

        widths = [40, 150, 120, 120, 80, 80, 60, 130]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

        self.tree.pack(fill="x", padx=20, pady=8)

    # ── ACTIONS ────────────────────────────────────────────
    def on_generate(self):
        customer = self.entry_customer.get().strip()
        event    = self.entry_event.get().strip()
        seat     = self.entry_seat.get().strip()
        amount   = self.entry_amount.get().strip()

        if not all([customer, event, seat, amount]):
            messagebox.showwarning("Missing", "Please fill all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        ticket_no = generate_ticket_no()

        # Save to DB
        save_ticket(customer, event, seat, amount, ticket_no)

        # Generate PDF
        pdf_path = generate_pdf_ticket(customer, event, seat, amount, ticket_no)

        # Clear form
        for attr in ["entry_customer", "entry_event", "entry_seat", "entry_amount"]:
            getattr(self, attr).delete(0, "end")

        self.refresh_table()
        messagebox.showinfo(
            " Ticket Created!",
            f"Ticket No: {ticket_no}\nPDF saved to: {pdf_path}"
        )

    def on_sync(self):
        count, message = sync_to_server()
        self.refresh_table()
        messagebox.showinfo("Sync Result", message)

    def on_open_folder(self):
        os.makedirs("output", exist_ok=True)
        if sys.platform == "win32":
            os.startfile("output")
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "output"])
        else:
            subprocess.Popen(["xdg-open", "output"])

    # ── REFRESH ────────────────────────────────────────────
    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for ticket in get_all_tickets():
            tid, customer, event, seat, amount, ticket_no, synced, created = ticket
            sync_icon = "✅" if synced else "⏳"
            self.tree.insert("", "end", values=(
                tid, ticket_no, customer, event,
                seat, format_currency(amount),
                sync_icon, created[:16]
            ))

    def refresh_status(self):
        if is_online():
            self.status_var.set("🟢 Online — Sync available")
        else:
            self.status_var.set("🔴 Offline — Saving locally to SQLite")
        self.root.after(5000, self.refresh_status)


# ── RUN ────────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = TicketApp(root)
    root.mainloop()