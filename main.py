import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
import re
from tkinter import filedialog, messagebox
from escpos.printer import Network
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
import os

def get_printer_ip():
    rc_path = os.path.join(os.path.dirname(__file__), "printer.rc")
    try:
        with open(rc_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "PRINTER_IP=" in line:
                    # Split on '=' and strip spaces
                    return line.split("=", 1)[1].strip()
    except Exception:
        pass
    return None

PRINTER_IP = get_printer_ip()  # Read IP from printer.rc


# Function to calculate totals, bill amounts, and return amount
def calculate(*args):
    try:
        # Calculate cash total
        bundles1 = [safe_eval(q.get()) for q in bundle1_vars]
        bundles2 = [safe_eval(b.get()) for b in bundle2_vars]
        bundles3 = [safe_eval(b.get()) for b in bundle3_vars]
        bundles4 = [safe_eval(b.get()) for b in bundle4_vars]
        bundles5 = [safe_eval(b.get()) for b in bundle5_vars]
        bundles6 = [safe_eval(b.get()) for b in bundle6_vars]
        quantities = [
            bundle1 + bundle2 + bundle3 + bundle4 + bundle5 + bundle6
            for bundle1, bundle2, bundle3, bundle4, bundle5, bundle6 in zip(
                bundles1, bundles2, bundles3, bundles4, bundles5, bundles6
            )
        ]
        amounts = [note * qty for note, qty in zip(notes, quantities)]
        for i, amt in enumerate(amounts):
            amount_vars[i].set(f"₹ {amt:.2f}")
        total_cash = sum(amounts)
        total_cash_var.set(f"₹ {total_cash:.2f}")

        # Get online payment value
        online_payment = safe_eval(online_payment_var.get())
        total = total_cash + online_payment
        total_var.set(f"₹ {total:.2f}")

        # Get bill values
        bill1 = safe_eval(bill1_var.get())
        bill2 = safe_eval(bill2_var.get())
        bill3 = safe_eval(bill3_var.get())

        # Calculate total payments and return amount
        total_bills = bill1 + bill2 + bill3
        return_amount = int(total - total_bills)  # Ensure return_amount is an integer

        # Update Return Amount and Color
        if return_amount == 0:
            return_var.set(f"₹ {return_amount}")
            return_label.config(fg="black")
        elif return_amount < 0:
            return_var.set(f"Take: ₹ {abs(return_amount)}")
            return_label.config(fg="red")  # Negative value: Red
        else:
            return_var.set(f"Give: ₹ {return_amount}")
            return_label.config(fg="green")  # Positive value: Green
    except Exception:
        total_var.set("Error")

# Function to clear all fields
def clear_all(*args):
    for var in bundle1_vars:
        var.set("")
    for var in bundle2_vars:
        var.set("")
    for var in bundle3_vars:
        var.set("")
    for var in bundle4_vars:
        var.set("")
    for var in bundle5_vars:  # NEW
        var.set("")  # NEW
    for var in bundle6_vars:  # NEW
        var.set("")  # NEW
    for var in amount_vars:
        var.set("₹ 0.00")
    bill1_var.set("")
    bill2_var.set("")
    bill3_var.set("")
    online_payment_var.set("")
    total_var.set("₹ 0.00")
    return_var.set("₹ 0.00")
    bill1_entry.focus()
    return_label.config(fg="black") # Reset to default color

# Function to move focus to the next widget
def focus_next_widget(event):
    widget = event.widget
    current_row = widget.grid_info()["row"]
    current_col = widget.grid_info()["column"]

    # Special case: Move focus from Bill 3 to Bundle 1 (2000 note)
    if current_row == 2 and current_col == 1:
        for child in widget.master.grid_slaves():
            if child.grid_info()["row"] == 4 and child.grid_info()["column"] == 1:
                child.focus()
                return "break"

    new_row = current_row + 1

    # Move focus vertically within the same column
    for child in widget.master.grid_slaves():
        if child.grid_info()["row"] == new_row and child.grid_info()["column"] == current_col:
            child.focus()
            return "break"

    # If at the end of the column, move to the next column and start from the top
    new_row = 4  # Starting row for the next column
    new_col = current_col + 1
    for child in widget.master.grid_slaves():
        if child.grid_info()["row"] == new_row and child.grid_info()["column"] == new_col:
            child.focus()
            return "break"

    return "break"

# Function to move focus to the previous widget
def focus_previous_widget(event):
    widget = event.widget
    current_row = widget.grid_info()["row"]
    current_col = widget.grid_info()["column"]
    new_row = current_row - 1

    # Move focus vertically within the same column
    for child in widget.master.grid_slaves():
        if child.grid_info()["row"] == new_row and child.grid_info()["column"] == current_col:
            child.focus()
            return "break"

    # If at the top of the column, move to the previous column and start from the bottom
    new_row = len(notes) + 3  # Ending row for the previous column
    new_col = current_col - 1
    for child in widget.master.grid_slaves():
        if child.grid_info()["row"] == new_row and child.grid_info()["column"] == new_col:
            child.focus()
            return "break"

    return "break"

# Function to move focus vertically (Up/Down arrow keys)
def focus_vertical(event):
    widget = event.widget
    try:
        current_row = int(widget.grid_info()["row"])
        current_col = int(widget.grid_info()["column"])
    except Exception:
        return "break"

    direction = -1 if event.keysym == "Up" else 1

    # Table starts at row 4, ends at row 13 (for 10 notes)
    min_row = 4
    max_row = min_row + len(notes) - 1

    new_row = current_row + direction

    # Stay within the table bounds
    if new_row < min_row or new_row > max_row:
        return "break"

    # Find the widget in the new row and same column
    for child in widget.master.grid_slaves():
        info = child.grid_info()
        if int(info["row"]) == new_row and int(info["column"]) == current_col:
            child.focus_set()
            return "break"
    return "break"

# Function to move focus horizontally (Left/Right arrow keys)
def focus_horizontal(event):
    widget = event.widget
    current_row = widget.grid_info()["row"]
    current_col = widget.grid_info()["column"]

    direction = -1 if event.keysym == "Left" else 1

    new_col = current_col + direction

    # Stay within the bounds of the grid (0 to 7 for columns)
    if new_col < 0 or new_col > 7:
        return "break"

    # Find the widget in the same row and new column
    for child in widget.master.grid_slaves():
        info = child.grid_info()
        if int(info["row"]) == current_row and int(info["column"]) == new_col:
            child.focus_set()
            return "break"
    return "break"

# Function to open Credit Card Charges Calculator
def open_credit_card_charges_calculator():
    def calculate_charges(*args):
        try:
            bill1 = safe_eval(bill1_entry.get())
            bill2 = safe_eval(bill2_entry.get())
            bill3 = safe_eval(bill3_entry.get())
            charges = safe_eval(charges_entry.get())

            total = bill1 + bill2 + bill3
            total_with_charges = total + (total * charges / 100)

            total_var.set(f"Total: ₹ {total:.2f}")
            total_with_charges_var.set(f"Total with Charges: ₹ {total_with_charges:.2f}")
            charges_display_var.set(f"Charges: ₹ {(total * charges / 100):.2f}")
        except Exception:
            total_var.set("Error")
            total_with_charges_var.set("Error")
            charges_display_var.set("Error")

    def clear_entries(*args):
        bill1_entry.delete(0, tk.END)
        bill2_entry.delete(0, tk.END)
        bill3_entry.delete(0, tk.END)
        charges_entry.delete(0, tk.END)
        charges_var.set(2.0)
        total_var.set("")
        total_with_charges_var.set("")
        charges_display_var.set("")
        bill1_entry.focus()

    # Create a new window for the calculator
    creditcardcalculator = tk.Toplevel(root)
    creditcardcalculator.title("Credit Card Charges Calculator")
    creditcardcalculator.geometry("500x400")  # Increased window size for better fit

    # Add widgets and functionality for the calculator here
    ttk.Label(creditcardcalculator, text="Credit Card Charges Calculator", font=("FiraCode Nerd Font", 13, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

    # Bill inputs
    ttk.Label(creditcardcalculator, text="Bill 1:", font=("FiraCode Nerd Font", 13, "bold")).grid(row=1, column=0, pady=5, sticky=tk.E)
    bill1_entry = ttk.Entry(creditcardcalculator, font=("FiraCode Nerd Font", 13, "bold"))
    bill1_entry.grid(row=1, column=1, pady=5)
    bill1_entry.bind("<KeyRelease>", calculate_charges)
    bill1_entry.bind("<Return>", focus_next_widget)
    bill1_entry.bind("<Shift-Tab>", focus_previous_widget)
    bill1_entry.bind("<Up>", focus_vertical)
    bill1_entry.bind("<Down>", focus_vertical)
    bill1_entry.bind("<Left>", focus_horizontal)
    bill1_entry.bind("<Right>", focus_horizontal)

    ttk.Label(creditcardcalculator, text="Bill 2:", font=("FiraCode Nerd Font", 13, "bold")).grid(row=2, column=0, pady=5, sticky=tk.E)
    bill2_entry = ttk.Entry(creditcardcalculator, font=("FiraCode Nerd Font", 13, "bold"))
    bill2_entry.grid(row=2, column=1, pady=5)
    bill2_entry.bind("<KeyRelease>", calculate_charges)
    bill2_entry.bind("<Return>", focus_next_widget)
    bill2_entry.bind("<Shift-Tab>", focus_previous_widget)
    bill2_entry.bind("<Up>", focus_vertical)
    bill2_entry.bind("<Down>", focus_vertical)
    bill2_entry.bind("<Left>", focus_horizontal)
    bill2_entry.bind("<Right>", focus_horizontal)

    ttk.Label(creditcardcalculator, text="Bill 3:", font=("FiraCode Nerd Font", 13, "bold")).grid(row=3, column=0, pady=5, sticky=tk.E)
    bill3_entry = ttk.Entry(creditcardcalculator, font=("FiraCode Nerd Font", 13, "bold"))
    bill3_entry.grid(row=3, column=1, pady=5)
    bill3_entry.bind("<KeyRelease>", calculate_charges)
    bill3_entry.bind("<Return>", focus_next_widget)
    bill3_entry.bind("<Shift-Tab>", focus_previous_widget)
    bill3_entry.bind("<Up>", focus_vertical)
    bill3_entry.bind("<Down>", focus_vertical)
    bill3_entry.bind("<Left>", focus_horizontal)
    bill3_entry.bind("<Right>", focus_horizontal)

    # Charges input with default value
    ttk.Label(creditcardcalculator, text="Charges (%):", font=("FiraCode Nerd Font", 13, "bold")).grid(row=4, column=0, pady=5, sticky=tk.E)
    charges_var = tk.DoubleVar(value=2.0)
    charges_entry = ttk.Entry(creditcardcalculator, textvariable=charges_var, font=("FiraCode Nerd Font", 13, "bold"))
    charges_entry.grid(row=4, column=1, pady=5)
    charges_entry.bind("<KeyRelease>", calculate_charges)
    charges_entry.bind("<Up>", focus_vertical)
    charges_entry.bind("<Down>", focus_vertical)

    # Labels to display results
    total_var = tk.StringVar()
    total_with_charges_var = tk.StringVar()
    charges_display_var = tk.StringVar()
    ttk.Label(creditcardcalculator, textvariable=total_var, font=("FiraCode Nerd Font", 13, "bold")).grid(row=5, column=0, columnspan=2, pady=5)
    ttk.Label(creditcardcalculator, textvariable=total_with_charges_var, font=("FiraCode Nerd Font", 13, "bold")).grid(row=6, column=0, columnspan=2, pady=5)
    ttk.Label(creditcardcalculator, textvariable=charges_display_var, font=("FiraCode Nerd Font", 13, "bold")).grid(row=7, column=0, columnspan=2, pady=5)

    # Bind Control+L to clear entries
    creditcardcalculator.bind('<Control-l>', clear_entries)
    creditcardcalculator.bind('<Control-L>', clear_entries)

def safe_eval(expr):
    # Allow only digits, +, -, *, /, parentheses, and spaces
    if re.fullmatch(r"[0-9+\-*/(). ]*", expr):
        try:
            return int(eval(expr, {"__builtins__": None}, {}))
        except Exception:
            return 0
    return 0

# GUI Setup
root = tk.Tk()
root.title("Cash Calculator")
root.geometry("1200x700")  # Adjusted window size for better fit

# Create a menubar
menubar = tk.Menu(root)
root.config(menu=menubar)

# Add Utilities menu
utilities_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Utilities", menu=utilities_menu)

# Add items to the Utilities menu
utilities_menu.add_command(label="Credit Card Charges Calculator", command=open_credit_card_charges_calculator)

# Bind Control+Shift+C to open the Credit Card Charges Calculator
root.bind('<Control-Shift-c>', lambda event: open_credit_card_charges_calculator())
root.bind('<Control-Shift-C>', lambda event: open_credit_card_charges_calculator())

# Data
notes = [2000, 500, 200, 100, 50, 20, 10, 5, 2, 1]
bundle1_vars = [tk.StringVar() for _ in notes]
bundle2_vars = [tk.StringVar() for _ in notes]
bundle3_vars = [tk.StringVar() for _ in notes]
bundle4_vars = [tk.StringVar() for _ in notes]
bundle5_vars = [tk.StringVar() for _ in notes]  # NEW
bundle6_vars = [tk.StringVar() for _ in notes]  # NEW
amount_vars = [tk.StringVar() for _ in notes]

# Bill 1
bill1_var = tk.StringVar()
ttk.Label(root, text="Bill 1", font=("FiraCode Nerd Font", 13, "bold")).grid(row=0, column=0, padx=5, pady=5)
bill1_entry = ttk.Entry(root, textvariable=bill1_var, font=("FiraCode Nerd Font", 13, "bold"), width=10)
bill1_entry.grid(row=0, column=1, padx=5, pady=5)
bill1_entry.bind("<KeyRelease>", calculate)
bill1_entry.bind("<Return>", focus_next_widget)
bill1_entry.bind("<Shift-Tab>", focus_previous_widget)
bill1_entry.bind("<Up>", focus_vertical)
bill1_entry.bind("<Down>", focus_vertical)
bill1_entry.bind("<Left>", focus_horizontal)
bill1_entry.bind("<Right>", focus_horizontal)

# Bill 2
bill2_var = tk.StringVar()
ttk.Label(root, text="Bill 2", font=("FiraCode Nerd Font", 13, "bold")).grid(row=1, column=0, padx=5, pady=5)
bill2_entry = ttk.Entry(root, textvariable=bill2_var, font=("FiraCode Nerd Font", 13, "bold"), width=10)
bill2_entry.grid(row=1, column=1, padx=5, pady=5)
bill2_entry.bind("<KeyRelease>", calculate)
bill2_entry.bind("<Return>", focus_next_widget)
bill2_entry.bind("<Shift-Tab>", focus_previous_widget)
bill2_entry.bind("<Up>", focus_vertical)
bill2_entry.bind("<Down>", focus_vertical)
bill2_entry.bind("<Left>", focus_horizontal)
bill2_entry.bind("<Right>", focus_horizontal)

# Bill 3
bill3_var = tk.StringVar()
ttk.Label(root, text="Bill 3", font=("FiraCode Nerd Font", 13, "bold")).grid(row=2, column=0, padx=5, pady=5)
bill3_entry = ttk.Entry(root, textvariable=bill3_var, font=("FiraCode Nerd Font", 13, "bold"), width=10)
bill3_entry.grid(row=2, column=1, padx=5, pady=5)
bill3_entry.bind("<KeyRelease>", calculate)
bill3_entry.bind("<Return>", focus_next_widget)
bill3_entry.bind("<Shift-Tab>", focus_previous_widget)
bill3_entry.bind("<Up>", focus_vertical)
bill3_entry.bind("<Down>", focus_vertical)
bill3_entry.bind("<Left>", focus_horizontal)
bill3_entry.bind("<Right>", focus_horizontal)

# Table Headers
ttk.Label(root, text="Notes", font=("FiraCode Nerd Font", 13, "bold"), width=10).grid(row=3, column=0)
ttk.Label(root, text="Bundle 1", font=("FiraCode Nerd Font", 13, "bold"), width=10).grid(row=3, column=1)
ttk.Label(root, text="Bundle 2", font=("FiraCode Nerd Font", 13, "bold"), width=10).grid(row=3, column=2)
ttk.Label(root, text="Bundle 3", font=("FiraCode Nerd Font", 13, "bold"), width=10).grid(row=3, column=3)
ttk.Label(root, text="Bundle 4", font=("FiraCode Nerd Font", 13, "bold"), width=10).grid(row=3, column=4)
ttk.Label(root, text="Bundle 5", font=("FiraCode Nerd Font", 13, "bold"), width=10).grid(row=3, column=5)  # NEW
ttk.Label(root, text="Bundle 6", font=("FiraCode Nerd Font", 13, "bold"), width=10).grid(row=3, column=6)  # NEW
ttk.Label(root, text="Amount", font=("FiraCode Nerd Font", 13, "bold"), width=10).grid(row=3, column=7)

# Table Rows
for i, note in enumerate(notes):
    ttk.Label(root, text=f"₹ {note}", font=("FiraCode Nerd Font", 13, "bold")).grid(row=i+4, column=0, padx=5, pady=5)
    bundle1_entry = ttk.Entry(root, textvariable=bundle1_vars[i], font=("FiraCode Nerd Font", 13, "bold"), width=10)
    bundle1_entry.grid(row=i+4, column=1, padx=5, pady=5)

    bundle2_entry = ttk.Entry(root, textvariable=bundle2_vars[i], font=("FiraCode Nerd Font", 13, "bold"), width=10)
    bundle2_entry.grid(row=i+4, column=2, padx=5, pady=5)

    bundle3_entry = ttk.Entry(root, textvariable=bundle3_vars[i], font=("FiraCode Nerd Font", 13, "bold"), width=10)
    bundle3_entry.grid(row=i+4, column=3, padx=5, pady=5)

    bundle4_entry = ttk.Entry(root, textvariable=bundle4_vars[i], font=("FiraCode Nerd Font", 13, "bold"), width=10)
    bundle4_entry.grid(row=i+4, column=4, padx=5, pady=5)

    bundle5_entry = ttk.Entry(root, textvariable=bundle5_vars[i], font=("FiraCode Nerd Font", 13, "bold"), width=10)  # NEW
    bundle5_entry.grid(row=i+4, column=5, padx=5, pady=5)  # NEW

    bundle6_entry = ttk.Entry(root, textvariable=bundle6_vars[i], font=("FiraCode Nerd Font", 13, "bold"), width=10)  # NEW
    bundle6_entry.grid(row=i+4, column=6, padx=5, pady=5)  # NEW

    # Bind navigation keys for all bundles
    for entry in [bundle1_entry, bundle2_entry, bundle3_entry, bundle4_entry, bundle5_entry, bundle6_entry]:
        entry.bind("<KeyRelease>", calculate)
        entry.bind("<Return>", focus_next_widget)
        entry.bind("<Shift-Tab>", focus_previous_widget)
        entry.bind("<Up>", focus_vertical)
        entry.bind("<Down>", focus_vertical)
        entry.bind("<Left>", focus_horizontal)
        entry.bind("<Right>", focus_horizontal)

    amount_label = ttk.Label(root, textvariable=amount_vars[i], font=("FiraCode Nerd Font", 13, "bold"), width=10)
    amount_label.grid(row=i+4, column=7, padx=5, pady=5)
    amount_vars[i].set("₹ 0.00")

# Online Payment (Above Total Cash)
online_payment_var = tk.StringVar()
ttk.Label(root, text="Online Payment", font=("FiraCode Nerd Font", 13, "bold")).grid(row=len(notes)+4, column=0, padx=5, pady=5)
online_payment_entry = ttk.Entry(root, textvariable=online_payment_var, font=("FiraCode Nerd Font", 13, "bold"), width=10)
online_payment_entry.grid(row=len(notes)+4, column=1, padx=5, pady=5)
online_payment_entry.bind("<KeyRelease>", calculate)
online_payment_entry.bind("<Return>", focus_next_widget)
online_payment_entry.bind("<Shift-Tab>", focus_previous_widget)
online_payment_entry.bind("<Up>", focus_vertical)
online_payment_entry.bind("<Down>", focus_vertical)
online_payment_entry.bind("<Left>", focus_horizontal)
online_payment_entry.bind("<Right>", focus_horizontal)

# Total Cash
ttk.Label(root, text="Total Cash:", font=("FiraCode Nerd Font", 13, "bold")).grid(row=len(notes)+5, column=0, padx=5, pady=5)
total_cash_var = tk.StringVar(value="₹ 0.00")
ttk.Label(root, textvariable=total_cash_var, font=("FiraCode Nerd Font", 13, "bold"), width=15).grid(row=len(notes)+5, column=7, padx=5, pady=5)

# Total Cash + Online Payment
total_var = tk.StringVar(value="₹ 0.00")
ttk.Label(root, text="Total (Cash + Online)", font=("FiraCode Nerd Font", 13, "bold")).grid(row=len(notes)+6, column=0, padx=5, pady=5)
ttk.Label(root, textvariable=total_var, font=("FiraCode Nerd Font", 13, "bold"), width=15).grid(row=len(notes)+6, column=7, padx=5, pady=5)

# Return Amount
ttk.Label(root, text="Return:", font=("FiraCode Nerd Font", 15, "bold")).grid(row=len(notes)+7, column=0,columnspan=2, padx=5, pady=5)
return_var = tk.StringVar(value="₹ 0")
return_label = tk.Label(root, textvariable=return_var, font=("FiraCode Nerd Font", 15, "bold"), width=15)
return_label.grid(row=len(notes)+7, column=1, columnspan=5, padx=5, pady=5)

# Function to save the cash receipt as PDF (optimized for 3-inch printer)
def save_receipt_pdf():
    receipt_lines = []
    receipt_lines.append("====== CASH RECEIPT ======")
    receipt_lines.append("")
    receipt_lines.append(f"Bill 1: {bill1_var.get()}")
    receipt_lines.append(f"Bill 2: {bill2_var.get()}")
    receipt_lines.append(f"Bill 3: {bill3_var.get()}")
    receipt_lines.append("")
    receipt_lines.append("Cash Breakdown:")
    for i, note in enumerate(notes):
        qty = (
            safe_eval(bundle1_vars[i].get())
            + safe_eval(bundle2_vars[i].get())
            + safe_eval(bundle3_vars[i].get())
            + safe_eval(bundle4_vars[i].get())
            + safe_eval(bundle5_vars[i].get())
            + safe_eval(bundle6_vars[i].get())
        )
        if qty > 0:
            total = note * qty
            receipt_lines.append(f"Rs.{note} x {qty} = Rs.{total}")
    receipt_lines.append("")
    receipt_lines.append(f"Online Payment: {online_payment_var.get()}")
    receipt_lines.append(f"Total Cash: {total_cash_var.get().replace('₹', 'Rs.')}")
    receipt_lines.append(f"Total (Cash + Online): {total_var.get().replace('₹', 'Rs.')}")
    receipt_lines.append(f"Return: {return_var.get().replace('₹', 'Rs.')}")
    receipt_lines.append("=========================")

    # --- Save as PDF optimized for 3-inch printer (72mm) ---
    pdf_width = 204  # 72mm in points
    line_height = 16
    margin = 8
    pdf_height = margin * 2 + line_height * (len(receipt_lines) + 2)

    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        title="Save Cash Receipt as PDF"
    )
    if file_path:
        try:
            c = canvas.Canvas(file_path, pagesize=(pdf_width, pdf_height))
            y = pdf_height - margin - line_height
            for line in receipt_lines:
                c.setFont("Helvetica-Bold", 10)
                c.drawString(margin, y, line)
                y -= line_height
            c.save()
            messagebox.showinfo("Receipt Saved", f"Receipt saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save receipt:\n{e}")

# Function to print the cash receipt to Epson POS printer
def print_pos_receipt():
    receipt_lines = []
    receipt_lines.append("====== CASH RECEIPT ======")
    receipt_lines.append("")
    receipt_lines.append(f"Bill 1: {bill1_var.get()}")
    receipt_lines.append(f"Bill 2: {bill2_var.get()}")
    receipt_lines.append(f"Bill 3: {bill3_var.get()}")
    receipt_lines.append("")
    receipt_lines.append("Cash Breakdown:")
    for i, note in enumerate(notes):
        qty = (
            safe_eval(bundle1_vars[i].get())
            + safe_eval(bundle2_vars[i].get())
            + safe_eval(bundle3_vars[i].get())
            + safe_eval(bundle4_vars[i].get())
            + safe_eval(bundle5_vars[i].get())
            + safe_eval(bundle6_vars[i].get())
        )
        if qty > 0:
            total = note * qty
            receipt_lines.append(f"Rs.{note} x {qty} = Rs.{total}")
    receipt_lines.append("")
    receipt_lines.append(f"Online Payment: {online_payment_var.get()}")
    receipt_lines.append(f"Total Cash: {total_cash_var.get().replace('₹', 'Rs.')}")
    receipt_lines.append(f"Total (Cash + Online): {total_var.get().replace('₹', 'Rs.')}")
    receipt_lines.append(f"Return: {return_var.get().replace('₹', 'Rs.')}")
    receipt_lines.append("=========================")

    receipt_text = "\n".join(receipt_lines)

    # --- Print to Epson POS printer using python-escpos ---
    try:
        if PRINTER_IP:
            p = Network(PRINTER_IP)
            p.set(align='center', font='a', width=2, height=2)
            p.text("CASH RECEIPT\n")
            p.set(align='left', font='a', width=1, height=1)
            p.text("\n")
            p.text(f"Bill 1: {bill1_var.get()}\n")
            p.text(f"Bill 2: {bill2_var.get()}\n")
            p.text(f"Bill 3: {bill3_var.get()}\n")
            p.text("\nCash Breakdown:\n")
            for i, note in enumerate(notes):
                qty = (
                    safe_eval(bundle1_vars[i].get())
                    + safe_eval(bundle2_vars[i].get())
                    + safe_eval(bundle3_vars[i].get())
                    + safe_eval(bundle4_vars[i].get())
                    + safe_eval(bundle5_vars[i].get())
                    + safe_eval(bundle6_vars[i].get())
                )
                if qty > 0:
                    total = note * qty
                    p.text(f"Rs.{note} x {qty} = Rs.{total}\n")
            p.text("\n")
            p.text(f"Online Payment: {online_payment_var.get()}\n")
            p.text(f"Total Cash: {total_cash_var.get().replace('₹', 'Rs.')}\n")
            p.text(f"Total (Cash + Online): {total_var.get().replace('₹', 'Rs.')}\n")
            p.text(f"Return: {return_var.get().replace('₹', 'Rs.')}\n")
            p.text("=========================\n")
            p.cut()
            messagebox.showinfo("Print", "Receipt sent to printer.")
        else:
            messagebox.showerror("Print Error", "Printer IP is not set. Please set PRINTER_IP at the top of the script.")
    except Exception as e:
        messagebox.showerror("Print Error", f"Could not print to EPSON printer:\n{e}")

# Add the Print Cash Receipt button (place after your Return label)
print_button = ttk.Button(
    root,
    text="Print Cash Receipt",
    command=print_pos_receipt,
    style="TButton"
)
print_button.grid(row=len(notes)+8, column=0, columnspan=4, pady=10)

# Add the Save PDF Receipt button (place after your Return label)
save_pdf_button = ttk.Button(
    root,
    text="Save PDF Receipt",
    command=save_receipt_pdf,
    style="TButton"
)
save_pdf_button.grid(row=len(notes)+8, column=4, columnspan=4, pady=10)

# Bind Ctrl+L to clear all
root.bind("<Control-l>", clear_all)
root.bind("<Control-L>", clear_all)

# Mainloop
root.mainloop()