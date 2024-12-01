import tkinter as tk
from tkinter import ttk

# Function to calculate total, bill amount, and return amount
def calculate(*args):
    try:
        quantities = [int(q.get()) if q.get() else 0 for q in qty_vars]
        amounts = [note * qty for note, qty in zip(notes, quantities)]
        for i, amt in enumerate(amounts):
            amount_vars[i].set(f"₹ {amt:.2f}")
        total = sum(amounts)
        total_var.set(f"₹ {total:.2f}")
        bill_amount = float(bill_amt_var.get()) if bill_amt_var.get() else 0
        return_amount = total - bill_amount
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
    bill_amt_var.set("")
    total_var.set("₹ 0.00")
    return_var.set("₹ 0.00")

# Function to move focus to the next widget
def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"  # Prevent the default behavior of the Enter key

# Function to move focus to the previous widget
def focus_previous_widget(event):
    event.widget.tk_focusPrev().focus()
    return "break"

# Function to move focus up or down based on arrow keys
def focus_vertical(event):
    widget = event.widget
    current_row = widget.grid_info()["row"]
    current_col = widget.grid_info()["column"]
    direction = -1 if event.keysym == "Up" else 1
    new_row = current_row + direction

    # Try to find a widget in the new row
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
    qty_entry.bind("<KeyRelease>", calculate)  # Trigger calculation on key press
    qty_entry.bind("<Return>", focus_next_widget)  # Move to the next field on Enter
    qty_entry.bind("<Shift-Tab>", focus_previous_widget)  # Move to the previous field on Shift+Tab
    qty_entry.bind("<Up>", focus_vertical)  # Move to the field above
    qty_entry.bind("<Down>", focus_vertical)  # Move to the field below

    amount_label = ttk.Label(root, textvariable=amount_vars[i], font=("Arial", 12), width=10)
    amount_label.grid(row=i+1, column=2, padx=5, pady=5)
    amount_vars[i].set("₹ 0.00")

# Total, Bill Amount, and Return
total_var = tk.StringVar(value="₹ 0.00")
return_var = tk.StringVar(value="₹ 0.00")
bill_amt_var = tk.StringVar()

ttk.Label(root, text="Total", font=("Arial", 12, "bold")).grid(row=len(notes)+1, column=0, padx=5, pady=5)
ttk.Label(root, textvariable=total_var, font=("Arial", 12), width=10).grid(row=len(notes)+1, column=2, padx=5, pady=5)

ttk.Label(root, text="Bill Amt", font=("Arial", 12, "bold")).grid(row=len(notes)+2, column=0, padx=5, pady=5)
bill_amt_entry = ttk.Entry(root, textvariable=bill_amt_var, font=("Arial", 12), width=10)
bill_amt_entry.grid(row=len(notes)+2, column=1, padx=5, pady=5)

# Bind navigation keys for the Bill Amount field
bill_amt_entry.bind("<KeyRelease>", calculate)  # Trigger calculation on key press
bill_amt_entry.bind("<Return>", focus_next_widget)  # Move to the next field on Enter
bill_amt_entry.bind("<Shift-Tab>", focus_previous_widget)  # Move to the previous field on Shift+Tab
bill_amt_entry.bind("<Up>", focus_vertical)  # Move to the field above
bill_amt_entry.bind("<Down>", focus_vertical)  # Move to the field below

ttk.Label(root, text="Return", font=("Arial", 12, "bold")).grid(row=len(notes)+3, column=0, padx=5, pady=5)
ttk.Label(root, textvariable=return_var, font=("Arial", 12), width=10).grid(row=len(notes)+3, column=2, padx=5, pady=5)

# Buttons
calc_button = ttk.Button(root, text="Calculate", command=calculate)
calc_button.grid(row=len(notes)+4, column=0, pady=10)

clear_button = ttk.Button(root, text="Clear", command=clear_all)
clear_button.grid(row=len(notes)+4, column=1, pady=10)

# Keyboard Shortcut for Clear
root.bind("<Control-l>", clear_all)

# Run the GUI
root.mainloop()
