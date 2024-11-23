import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import threading
import time

# Simulation variables
days = 1
bull_days = 0
bear_days = 0
bull_days_count = 0
bear_days_count = 0
Money = 200
shares_owned = 0
holdings_value = 0
stock_price = 100
price_history = [stock_price]

# Tkinter GUI setup
window = tk.Tk()
window.title("Stock Market Simulator")
window.geometry("800x600")

# Styles
style = ttk.Style(window)
style.theme_use("clam")
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 10, "bold"))
style.configure("Header.TLabel", font=("Arial", 16, "bold"))

# Frames
header_frame = ttk.Frame(window)
header_frame.pack(fill=tk.X, pady=10)

left_frame = ttk.Frame(window, padding=10)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

right_frame = ttk.Frame(window, padding=10)
right_frame.pack(side=tk.RIGHT, fill=tk.Y)

# Header
header = ttk.Label(header_frame, text="Stock Market Simulator", style="Header.TLabel")
header.pack()

# Left frame (Graph)
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=left_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

# Right frame (Controls)
info_frame = ttk.Frame(right_frame)
info_frame.pack(fill=tk.X, pady=10)

# Labels for money, shares, and holdings value
money_label = ttk.Label(info_frame, text=f"Capital: ${Money:.2f}")
money_label.pack(anchor=tk.W)

shares_label = ttk.Label(info_frame, text=f"Shares Owned: {shares_owned}")
shares_label.pack(anchor=tk.W)

holding_label = ttk.Label(info_frame, text=f"Holdings Value: ${holdings_value:.2f}")
holding_label.pack(anchor=tk.W)

price_label = ttk.Label(info_frame, text=f"Current Price: ${price_history[-1]:.2f}")
price_label.pack(anchor=tk.W)

# Input and buttons
input_label = ttk.Label(right_frame, text="Number of Shares:")
input_label.pack(pady=5)

input = ttk.Entry(right_frame)
input.pack(pady=5)

button_frame = ttk.Frame(right_frame)
button_frame.pack(pady=10)

buy_button = ttk.Button(button_frame, text="Buy", command=lambda: handle_transaction("buy"))
buy_button.grid(row=0, column=0, padx=5)

sell_button = ttk.Button(button_frame, text="Sell", command=lambda: handle_transaction("sell"))
sell_button.grid(row=0, column=1, padx=5)

# Popup for warnings
def open_popup(message):
    popup = tk.Toplevel(window)
    popup.title("Warning")
    ttk.Label(popup, text=message, wraplength=250).pack(pady=20)
    ttk.Button(popup, text="OK", command=popup.destroy).pack(pady=10)

# Buy/Sell transaction handler
def handle_transaction(action):
    global Money, shares_owned
    try:
        amount = int(input.get())
        if amount <= 0:
            open_popup("Enter a positive number of shares.")
            return

        if action == "buy":
            total_cost = amount * price_history[-1]
            if total_cost > Money:
                open_popup("Insufficient funds!")
                return
            Money -= total_cost
            shares_owned += amount
        elif action == "sell":
            if shares_owned < amount:
                open_popup("You don't own enough shares.")
                return
            total_earnings = amount * price_history[-1]
            Money += total_earnings
            shares_owned -= amount

        update_ui()
    except ValueError:
        open_popup("Please enter a valid number.")
    finally:
        # Clear the input field
        input.delete(0, tk.END)

# Update UI
def update_ui():
    global holdings_value
    holdings_value = shares_owned * price_history[-1]
    money_label.config(text=f"Capital: ${Money:.2f}")
    shares_label.config(text=f"Shares Owned: {shares_owned}")
    holding_label.config(text=f"Holdings Value: ${holdings_value:.2f}")
    price_label.config(text=f"Current Price: ${price_history[-1]:.2f}")

# Stock price simulation
def simulate_stock_prices():
    global days, bull_days, bear_days, bull_days_count, bear_days_count, stock_price, price_history
    while stock_price > 0 and days <= 30:
        fluctuation = random.uniform(-5, 5)
        stock_price = max(stock_price + fluctuation, 0)
        price_history.append(stock_price)

        ax.clear()
        ax.plot(price_history, marker="o", label="Stock Price")
        ax.set_title("Stock Price Simulation")
        ax.set_xlabel("Day")
        ax.set_ylabel("Price ($)")
        ax.legend()
        ax.grid(True)
        canvas.draw()

        days += 1
        update_ui()
        time.sleep(1)

# Start simulation thread
simulation_thread = threading.Thread(target=simulate_stock_prices, daemon=True)
simulation_thread.start()

# Run the Tkinter event loop
window.mainloop()
