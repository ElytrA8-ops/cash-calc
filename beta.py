import tkinter as tk
from tkinter import ttk

# Function to calculate total, bill amounts, and return amount
def calculate(*args):
    try:
        quantities = [int(q.get()) if q.get() else 0 for q in qty_vars]
        amounts = [note * qty for note, qty in zip(notes, quantities)]
        for i, amt in enumerate(amounts):
            amount_vars[i].set(f"₹ {amt:.2f}")
        total = sum(amounts)
        total_var.set(f"₹ {total:.2f}")

        # Get bill and payment values
        bill1 = float(bill1_var.get()) if bill1_var.get() else 0
        bill2 = float(bill2_var.get()) if bill2_var.get() else 0
        bill3 = float(bill3_var.get()) if bill3_var.get() else 0
        online_payment = float(online_payment_var.get()) if online_payment_var.get() else 0

        # Calculate total payments and return amount
        total_payments = bill1 + bill2 + bill3 + online_payment
        return_amount = total - total_payments

        return_var.set(f"₹ {return_amount:.2f}")
    except ValueError:
        total_var.set("Error")
        return_var.set("Error")

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
    for child in root.grid_slaves():
        if child.grid_info()["row"] == new_row and child.grid_info()["column"] == current_col:
            child.focus()
            break
    return "break"

# GUI Setup
root = tk.Tk()
root.title("Cash Calculator")

# Data
notes = [2000, 500, 200, 100, 50, 20, 10, 5, 2, 1]
qty_vars = [tk.StringVar() for _ in notes]
amount_vars = [tk.StringVar() for _ in notes]

# Table Headers
ttk.Label(root, text="Notes", font=("Arial", 12, "bold"), width=10).grid(row=0, column=0)
ttk.Label(root, text="Quantity", font=("Arial", 12, "bold"), width=10).grid(row=0, column=1)
ttk.Label(root, text="Amount", font=("Arial", 12, "bold"), width=10).grid(row=0, column=2)

# Table Rows
for i, note in enumerate(notes):
    ttk.Label(root, text=f"₹ {note}", font=("Arial", 12)).grid(row=i+1, column=0, padx=5, pady=5)
    qty_entry = ttk.Entry(root, textvariable=qty_vars[i], font=("Arial", 12), width=10)
    qty_entry.grid(row=i+1, column=1, padx=5, pady=5)

    # Bind navigation keys
    qty_entry.bind("<KeyRelease>", calculate)
    qty_entry.bind("<Return>", focus_next_widget)
    qty_entry.bind("<Shift-Tab>", focus_previous_widget)
    qty_entry.bind("<Up>", focus_vertical)
    qty_entry.bind("<Down>", focus_vertical)

    amount_label = ttk.Label(root, textvariable=amount_vars[i], font=("Arial", 12), width=10)
    amount_label.grid(row=i+1, column=2, padx=5, pady=5)
    amount_vars[i].set("₹ 0.00")

# Total Cash
total_var = tk.StringVar(value="₹ 0.00")
ttk.Label(root, text="Total", font=("Arial", 12, "bold")).grid(row=len(notes)+1, column=0, padx=5, pady=5)
ttk.Label(root, textvariable=total_var, font=("Arial", 12), width=10).grid(row=len(notes)+1, column=2, padx=5, pady=5)

# Bill 1
bill1_var = tk.StringVar()
ttk.Label(root, text="Bill 1", font=("Arial", 12, "bold")).grid(row=len(notes)+2, column=0, padx=5, pady=5)
bill1_entry = ttk.Entry(root, textvariable=bill1_var, font=("Arial", 12), width=10)
bill1_entry.grid(row=len(notes)+2, column=1, padx=5, pady=5)
bill1_entry.bind("<KeyRelease>", calculate)

# Bill 2
bill2_var = tk.StringVar()
ttk.Label(root, text="Bill 2", font=("Arial", 12, "bold")).grid(row=len(notes)+3, column=0, padx=5, pady=5)
bill2_entry = ttk.Entry(root, textvariable=bill2_var, font=("Arial", 12), width=10)
bill2_entry.grid(row=len(notes)+3, column=1, padx=5, pady=5)
bill2_entry.bind("<KeyRelease>", calculate)

# Bill 3
bill3_var = tk.StringVar()
ttk.Label(root, text="Bill 3", font=("Arial", 12, "bold")).grid(row=len(notes)+4, column=0, padx=5, pady=5)
bill3_entry = ttk.Entry(root, textvariable=bill3_var, font=("Arial", 12), width=10)
bill3_entry.grid(row=len(notes)+4, column=1, padx=5, pady=5)
bill3_entry.bind("<KeyRelease>", calculate)

# Online Payment
online_payment_var = tk.StringVar()
ttk.Label(root, text="Online Payment", font=("Arial", 12, "bold")).grid(row=len(notes)+5, column=0, padx=5, pady=5)
online_payment_entry = ttk.Entry(root, textvariable=online_payment_var, font=("Arial", 12), width=10)
online_payment_entry.grid(row=len(notes)+5, column=1, padx=5, pady=5)
online_payment_entry.bind("<KeyRelease>", calculate)

# Return Amount
return_var = tk.StringVar(value="₹ 0.00")
ttk.Label(root, text="Return", font=("Arial", 12, "bold")).grid(row=len(notes)+6, column=0, padx=5, pady=5)
ttk.Label(root, textvariable=return_var, font=("Arial", 12), width=10).grid(row=len(notes)+6, column=2, padx=5, pady=5)

# Buttons
calc_button = ttk.Button(root, text="Calculate", command=calculate)
calc_button.grid(row=len(notes)+7, column=0, pady=10)

clear_button = ttk.Button(root, text="Clear", command=clear_all)
clear_button.grid(row=len(notes)+7, column=1, pady=10)

# Keyboard Shortcut for Clear
root.bind("<Control-l>", clear_all)

# Run the GUI
root.mainloop()