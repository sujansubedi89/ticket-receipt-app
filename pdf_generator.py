# pdf_generator.py
from fpdf import FPDF
from datetime import datetime
import os


def generate_pdf_ticket(customer, event, seat, amount, ticket_no):
    """Generate a PDF ticket and save to output folder"""

    os.makedirs("output", exist_ok=True)

    pdf = FPDF()
    pdf.add_page()

    # Header background
    pdf.set_fill_color(30, 30, 60)
    pdf.rect(0, 0, 210, 40, 'F')

    # Header text
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 22)
    pdf.set_xy(0, 10)
    pdf.cell(210, 10, "EVENT TICKET", align="C")

    pdf.set_font("Arial", "", 11)
    pdf.set_xy(0, 25)
    pdf.cell(210, 10, "Powered by Websoft Ticket System", align="C")

    # Ticket details
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(20, 55)

    details = [
        ("Ticket No",  ticket_no),
        ("Customer",   customer),
        ("Event",      event),
        ("Seat",       seat),
        ("Amount",     f"Npr{amount:,.2f}"),
        ("Date",       datetime.now().strftime("%Y-%m-%d %H:%M")),
        ("Status",     "CONFIRMED"),
    ]

    for label, value in details:
        pdf.set_font("Arial", "B", 11)
        pdf.set_x(20)
        pdf.cell(50, 12, f"{label}:", border=0)

        pdf.set_font("Arial", "", 11)
        pdf.cell(120, 12, str(value), border=0)
        pdf.ln()

    # Divider line
    pdf.set_draw_color(200, 200, 200)
    pdf.line(20, pdf.get_y() + 5, 190, pdf.get_y() + 5)

    # Footer
    pdf.set_xy(20, pdf.get_y() + 15)
    pdf.set_font("Arial", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 10, "Official ticket. Present at entry. Non-transferable.", align="C")

    # Save file
    filename = f"output/{ticket_no}.pdf"
    pdf.output(filename)
    print(f"PDF saved: {filename}")
    return filename