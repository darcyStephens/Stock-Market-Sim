import random
import matplotlib.pyplot as plt
import numpy as np

days = 1
bull_days = 0
bear_days = 0
bull_days_count = 0
bear_days_count = 0

stock_price = 10
price_history = [stock_price]


while stock_price > 0 and days < 20:

    #default market movement
    fluctuation = random.randrange(-10,10)
    factor = random.random()
    stock_price = stock_price + (fluctuation*factor)

    #checking for price change
    if stock_price > price_history[-1]:
        bull_days +=1
        bull_days_count +=1
    else:
        bear_days +=1
        bear_days_count +=1
    
    #bull market
    if bull_days >= 3 or bear_days >=4:
        stock_price = stock_price * 1.05
        bull_days = bull_days * 0.2
        print("bull market")
    #bear market
    if bear_days >= 3 or bull_days >= 4:
        stock_price = stock_price * 0.95
        bear_days = bear_days * 0.2
        print("bear market")

    if stock_price < 0:
        break

    stock_price = float("{:.2f}".format(stock_price))
    price_history.append(stock_price)
    days +=1

print(price_history)
print("bull days ", bull_days_count)
print("bear days ", bear_days_count)

xpoints = np.arange(len(price_history))
ypoints = np.array(price_history)
plt.plot(xpoints, ypoints, marker="o", label="Stock Price")
plt.xlabel("Day")
plt.ylabel("Stock Price")
plt.title("Stock Price Simulation")
plt.legend()
plt.grid(True)
plt.savefig("stock_price_simulation.png")