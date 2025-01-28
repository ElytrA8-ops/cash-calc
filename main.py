import tkinter as tk
from tkinter import ttk

# Function to calculate totals, bill amounts, and return amount
def calculate(*args):
    try:
        # Calculate cash total
        quantities = [int(q.get()) if q.get() else 0 for q in qty_vars]
        amounts = [note * qty for note, qty in zip(notes, quantities)]
        for i, amt in enumerate(amounts):
            amount_vars[i].set(f"₹ {amt:.2f}")
        total_cash = sum(amounts)
        total_cash_var.set(f"₹ {total_cash:.2f}")

        # Get online payment value
        online_payment = float(online_payment_var.get()) if online_payment_var.get() else 0
        total = total_cash + online_payment
        total_var.set(f"₹ {total:.2f}")

        # Get bill values
        bill1 = float(bill1_var.get()) if bill1_var.get() else 0
        bill2 = float(bill2_var.get()) if bill2_var.get() else 0
        bill3 = float(bill3_var.get()) if bill3_var.get() else 0

        # Calculate total payments and return amount
        total_bills = bill1 + bill2 + bill3
        return_amount = int(total - total_bills)  # Ensure return_amount is an integer

        # Update Return Amount and Color
        return_var.set(f"₹ {return_amount}")
        if return_amount < 0:
            return_label.config(fg="red")  # Negative value: Red
        else:
            return_label.config(fg="green")  # Positive value: Green
    except ValueError:
        total_var.set("Error")

# Function to clear all fields
def clear_all(*args):
    for var in qty_vars:
        var.set("")
    for var in amount_vars:
        var.set("₹ 0.00")
    bill1_var.set("")
    bill2_var.set("")
    bill3_var.set("")
    online_payment_var.set("")
    total_var.set("₹ 0.00")
    return_var.set("₹ 0.00")
    qty_entries[1].focus()
    return_label.config(fg="black") # Reset to default color

# Function to move focus to the next widget
def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"

# Function to move focus to the previous widget
def focus_previous_widget(event):
    event.widget.tk_focusPrev().focus()
    return "break"

# Function to move focus vertically (Up/Down arrow keys)
def focus_vertical(event):
    widget = event.widget
    current_row = widget.grid_info()["row"]
    current_col = widget.grid_info()["column"]
    direction = -1 if event.keysym == "Up" else 1
    new_row = current_row + direction
    for child in widget.master.grid_slaves():
        if child.grid_info()["row"] == new_row and child.grid_info()["column"] == current_col:
            child.focus()
            break
    return "break"

# Function to open Credit Card Charges Calculator
def open_credit_card_charges_calculator():
    def calculate_charges(*args):
        try:
            bill1 = float(bill1_entry.get()) if bill1_entry.get() else 0
            bill2 = float(bill2_entry.get()) if bill2_entry.get() else 0
            bill3 = float(bill3_entry.get()) if bill3_entry.get() else 0
            charges = float(charges_var.get())

            total = bill1 + bill2 + bill3
            total_with_charges = total + (total * charges / 100)

            total_var.set(f"Total: ₹ {total:.2f}")
            total_with_charges_var.set(f"Total with Charges: ₹ {total_with_charges:.2f}")
        except ValueError:
            total_var.set("Error")
            total_with_charges_var.set("Error")

    def clear_entries(*args):
        bill1_entry.delete(0, tk.END)
        bill2_entry.delete(0, tk.END)
        bill3_entry.delete(0, tk.END)
        charges_entry.delete(0, tk.END)
        charges_var.set(2.0)
        total_var.set("")
        total_with_charges_var.set("")
        bill1_entry.focus()

    # Create a new window for the calculator
    creditcardcalculator = tk.Toplevel(root)
    creditcardcalculator.title("Credit Card Charges Calculator")
    creditcardcalculator.geometry("300x300")

    # Add widgets and functionality for the calculator here
    ttk.Label(creditcardcalculator, text="Credit Card Charges Calculator", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

    # Bill inputs
    ttk.Label(creditcardcalculator, text="Bill 1:").grid(row=1, column=0, pady=5, sticky=tk.E)
    bill1_entry = ttk.Entry(creditcardcalculator)
    bill1_entry.grid(row=1, column=1, pady=5)
    bill1_entry.bind("<KeyRelease>", calculate_charges)
    bill1_entry.bind("<Return>", focus_next_widget)
    bill1_entry.bind("<Shift-Tab>", focus_previous_widget)
    bill1_entry.bind("<Up>", focus_vertical)
    bill1_entry.bind("<Down>", focus_vertical)

    ttk.Label(creditcardcalculator, text="Bill 2:").grid(row=2, column=0, pady=5, sticky=tk.E)
    bill2_entry = ttk.Entry(creditcardcalculator)
    bill2_entry.grid(row=2, column=1, pady=5)
    bill2_entry.bind("<KeyRelease>", calculate_charges)
    bill2_entry.bind("<Return>", focus_next_widget)
    bill2_entry.bind("<Shift-Tab>", focus_previous_widget)
    bill2_entry.bind("<Up>", focus_vertical)
    bill2_entry.bind("<Down>", focus_vertical)

    ttk.Label(creditcardcalculator, text="Bill 3:").grid(row=3, column=0, pady=5, sticky=tk.E)
    bill3_entry = ttk.Entry(creditcardcalculator)
    bill3_entry.grid(row=3, column=1, pady=5)
    bill3_entry.bind("<KeyRelease>", calculate_charges)
    bill3_entry.bind("<Return>", focus_next_widget)
    bill3_entry.bind("<Shift-Tab>", focus_previous_widget)
    bill3_entry.bind("<Up>", focus_vertical)
    bill3_entry.bind("<Down>", focus_vertical)

    # Charges input with default value
    ttk.Label(creditcardcalculator, text="Charges (%):").grid(row=4, column=0, pady=5, sticky=tk.E)
    charges_var = tk.DoubleVar(value=2.0)
    charges_entry = ttk.Entry(creditcardcalculator, textvariable=charges_var)
    charges_entry.grid(row=4, column=1, pady=5)
    charges_entry.bind("<KeyRelease>", calculate_charges)
    charges_entry.bind("<Up>", focus_vertical)
    charges_entry.bind("<Down>", focus_vertical)

    # Labels to display results
    total_var = tk.StringVar()
    total_with_charges_var = tk.StringVar()
    ttk.Label(creditcardcalculator, textvariable=total_var).grid(row=5, column=0, columnspan=2, pady=5)
    ttk.Label(creditcardcalculator, textvariable=total_with_charges_var).grid(row=6, column=0, columnspan=2, pady=5)

    # Bind Control+L to clear entries
    creditcardcalculator.bind('<Control-l>', clear_entries)
    creditcardcalculator.bind('<Control-L>', clear_entries)

# GUI Setup
root = tk.Tk()
root.title("Cash Calculator")
root.geometry("400x600")  # Adjust initial window size

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
qty_vars = [tk.StringVar() for _ in notes]
amount_vars = [tk.StringVar() for _ in notes]

# Table Headers
ttk.Label(root, text="Notes", font=("Arial", 12, "bold"), width=10).grid(row=0, column=0)
ttk.Label(root, text="Quantity", font=("Arial", 12, "bold"), width=10).grid(row=0, column=1)
ttk.Label(root, text="Amount", font=("Arial", 12, "bold"), width=10).grid(row=0, column=2)

# Table Rows
qty_entries = []
for i, note in enumerate(notes):
    ttk.Label(root, text=f"₹ {note}", font=("Arial", 12)).grid(row=i+1, column=0, padx=5, pady=5)
    qty_entry = ttk.Entry(root, textvariable=qty_vars[i], font=("Arial", 12), width=10)
    qty_entry.grid(row=i+1, column=1, padx=5, pady=5)
    qty_entries.append(qty_entry)

    # Bind navigation keys
    qty_entry.bind("<KeyRelease>", calculate)
    qty_entry.bind("<Return>", focus_next_widget)
    qty_entry.bind("<Shift-Tab>", focus_previous_widget)
    qty_entry.bind("<Up>", focus_vertical)
    qty_entry.bind("<Down>", focus_vertical)

    amount_label = ttk.Label(root, textvariable=amount_vars[i], font=("Arial", 12), width=10)
    amount_label.grid(row=i+1, column=2, padx=5, pady=5)
    amount_vars[i].set("₹ 0.00")

# Online Payment (Above Total Cash)
online_payment_var = tk.StringVar()
ttk.Label(root, text="Online Payment", font=("Arial", 12, "bold")).grid(row=len(notes)+1, column=0, padx=5, pady=5)
online_payment_entry = ttk.Entry(root, textvariable=online_payment_var, font=("Arial", 12), width=10)
online_payment_entry.grid(row=len(notes)+1, column=1, padx=5, pady=5)
online_payment_entry.bind("<KeyRelease>", calculate)
online_payment_entry.bind("<Return>", focus_next_widget)
online_payment_entry.bind("<Shift-Tab>", focus_previous_widget)
online_payment_entry.bind("<Up>", focus_vertical)
online_payment_entry.bind("<Down>", focus_vertical)

# Total Cash
ttk.Label(root, text="Total Cash:", font=("Arial", 12, "bold")).grid(row=len(notes)+2, column=0, padx=5, pady=5)
total_cash_var = tk.StringVar(value="₹ 0.00")
ttk.Label(root, textvariable=total_cash_var, font=("Arial", 12, "bold"), width=15).grid(row=len(notes)+2, column=2, padx=5, pady=5)

# Total Cash + Online Payment
total_var = tk.StringVar(value="₹ 0.00")
ttk.Label(root, text="Total (Cash + Online)", font=("Arial", 12, "bold")).grid(row=len(notes)+3, column=0, padx=5, pady=5)
ttk.Label(root, textvariable=total_var, font=("Arial", 12, "bold"), width=15).grid(row=len(notes)+3, column=2, padx=5, pady=5)

# Bill 1
bill1_var = tk.StringVar()
ttk.Label(root, text="Bill 1", font=("Arial", 12, "bold")).grid(row=len(notes)+4, column=0, padx=5, pady=5)
bill1_entry = ttk.Entry(root, textvariable=bill1_var, font=("Arial", 12), width=10)
bill1_entry.grid(row=len(notes)+4, column=1, padx=5, pady=5)
bill1_entry.bind("<KeyRelease>", calculate)
bill1_entry.bind("<Return>", focus_next_widget)
bill1_entry.bind("<Shift-Tab>", focus_previous_widget)
bill1_entry.bind("<Up>", focus_vertical)
bill1_entry.bind("<Down>", focus_vertical)

# Bill 2
bill2_var = tk.StringVar()
ttk.Label(root, text="Bill 2", font=("Arial", 12, "bold")).grid(row=len(notes)+5, column=0, padx=5, pady=5)
bill2_entry = ttk.Entry(root, textvariable=bill2_var, font=("Arial", 12), width=10)
bill2_entry.grid(row=len(notes)+5, column=1, padx=5, pady=5)
bill2_entry.bind("<KeyRelease>", calculate)
bill2_entry.bind("<Return>", focus_next_widget)
bill2_entry.bind("<Shift-Tab>", focus_previous_widget)
bill2_entry.bind("<Up>", focus_vertical)
bill2_entry.bind("<Down>", focus_vertical)

# Bill 3
bill3_var = tk.StringVar()
ttk.Label(root, text="Bill 3", font=("Arial", 12, "bold")).grid(row=len(notes)+6, column=0, padx=5, pady=5)
bill3_entry = ttk.Entry(root, textvariable=bill3_var, font=("Arial", 12), width=10)
bill3_entry.grid(row=len(notes)+6, column=1, padx=5, pady=5)
bill3_entry.bind("<KeyRelease>", calculate)
bill3_entry.bind("<Return>", focus_next_widget)
bill3_entry.bind("<Shift-Tab>", focus_previous_widget)
bill3_entry.bind("<Up>", focus_vertical)
bill3_entry.bind("<Down>", focus_vertical)

# Return Amount
ttk.Label(root, text="Return:", font=("Arial", 15, "bold")).grid(row=len(notes)+7, column=0,columnspan=2, padx=5, pady=5)
return_var = tk.StringVar(value="₹ 0")
return_label = tk.Label(root, textvariable=return_var, font=("Arial", 15, "bold"), width=15)
return_label.grid(row=len(notes)+7, column=1, columnspan=3, padx=5, pady=5)

# Bind Ctrl+L to clear all
root.bind("<Control-l>", clear_all)
root.bind("<Control-L>", clear_all)

# Mainloop
root.mainloop()