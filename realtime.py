import tkinter as tk
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
Money = 100
shares_owned = 0
holdings_value = 0


stock_price = 100
price_history = [stock_price]

# Tkinter GUI setup
window = tk.Tk()
window.title("Stock Market Simulator")

# Add a header label
header = tk.Label(window, text="Stock Market Simulator")
header.pack()

# Setting up frames
price_frame = tk.Frame(master=window, width=400, height=400, bg="white")
price_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

# Input and button setup
input_label = tk.Label(window, text="Number of shares")
input_label.pack()
input = tk.Entry(window)
input.pack()

#displaying money and shares owned
money_label = tk.Label(window, text=f"Capital: ${Money:.2f}")
money_label.pack()

shares_label = tk.Label(window, text=f"Shares Owned: ${shares_owned}")
shares_label.pack()

holding_label = tk.Label(window, text=f"Holdings value: ${holdings_value:.2f}")
holding_label.pack()


# Handle Buy button click
def handle_buy():
    global Money, shares_owned
    try:
        amount = int(input.get())
        total_cost = amount * price_history[-1]
        if total_cost > Money:
            print("Insufficient funds! Transaction denied.")
            return
        Money -= total_cost
        shares_owned += amount
        print(f"Bought {amount} shares at ${price_history[-1]} each")
        update_labels()
        value_calc_update()
    except ValueError:
        print("Enter a valid number of shares")
    input.delete(0, tk.END)


# Handle Sell button click
def handle_sell():
    global Money, shares_owned
    try:
        amount = int(input.get())
        if amount <= 0:
            print("Enter a positive number of shares to sell.")
            return
        if shares_owned >= amount:
            total_earnings = amount * price_history[-1]
            Money += total_earnings
            shares_owned -= amount
            print(f"Sold {amount} shares at ${price_history[-1]} each")
            update_labels()
            value_calc_update()
        else:
            print("You are trying to sell more shares than you own.")
    except ValueError:
        print("Enter a valid number of shares.")
    input.delete(0, tk.END)


def update_labels():
    money_label.config(text=f"Capital: ${Money:.2f}")
    shares_label.config(text=f"Shares Owned: {shares_owned}")
    
def value_calc_update():
    global holdings_value, shares_owned
    holdings_value = price_history[-1] * shares_owned
    window.after(0, lambda: holding_label.config(text=f"Holdings value: ${holdings_value:.2f}"))


buy = tk.Button(window, text="Buy", width=25, height=5, bg="green", command=handle_buy)
buy.pack()
sell = tk.Button(window, text="Sell", width=25, height=5, bg="red", command=handle_sell)
sell.pack()

# Matplotlib setup
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=price_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

# Simulation function
def simulate_stock_prices():
    global days, bull_days, bear_days, bull_days_count, bear_days_count, stock_price, price_history, Money, shares_owned

    while stock_price > 0 and days <= 30:
        # Simulate stock price fluctuation
        fluctuation = random.randrange(-10, 10)
        factor = random.random()
        stock_price += fluctuation * factor

        # Check price movement
        if stock_price > price_history[-1]:
            bull_days += 1
            bull_days_count += 1
        else:
            bear_days += 1
            bear_days_count += 1

        # Handle bull and bear market adjustments
        if bull_days >= 3 or bear_days >= 4:
            stock_price *= 1.05
            bull_days *= 0.2
        if bear_days >= 3 or bull_days >= 4:
            stock_price *= 0.95
            bear_days *= 0.2

        # Ensure stock price is positive
        stock_price = max(stock_price, 0)
        stock_price = float("{:.2f}".format(stock_price))
        price_history.append(stock_price)

        # Update the plot
        ax.clear()
        ax.plot(price_history, marker="o", label="Stock Price")
        ax.set_xlabel("Day")
        ax.set_ylabel("Stock Price")
        ax.set_title("Stock Price Simulation")
        ax.legend()
        ax.grid(True)
        canvas.draw()

        # Increment day and delay
        days += 1
        value_calc_update()
        time.sleep(1)

    print("Simulation ended.")
    print("Price history:", price_history)
    print("Bull days:", bull_days_count)
    print("Bear days:", bear_days_count)

# Run the simulation in a separate thread
simulation_thread = threading.Thread(target=simulate_stock_prices, daemon=True)
simulation_thread.start()

# Run the Tkinter main loop
window.mainloop()
