import tkinter as tk

def handle_buy():
    global amount
    amount = input.get()  # Get the text from the input box
    print(amount)         # Print the amount
    input.delete(0, tk.END)  # Clear the input box

def handle_sell():
    amount = input.get()
    print(amount)
    input.delete(0, tk.END)

# Create the main window
window = tk.Tk()

# Add a header label
header = tk.Label(window, text='Stock Market Simulator')
header.pack()  # Adding widget to window


#setting up frames
price_frame = tk.Frame(master=window, width = 200, height = 200, bg="white")
price_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

# Add input label and entry
input_label = tk.Label(window, text="Number of shares")
input = tk.Entry(window)
input_label.pack()
input.pack()

# Add the "Buy" button and connect it to the handle_buy function
buy = tk.Button(window, text="Buy", width=25, height=5, bg="green", command=handle_buy)
buy.pack()

# Add the "Buy" button and connect it to the handle_buy function
sell = tk.Button(window, text="Sell", width=25, height=5, bg="red", command=handle_sell)
sell.pack()

# Run the main loop
window.mainloop()
