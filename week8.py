"""
Author:         Mauricio Beltran
Date:           5/26/2023
Functionality:

This functionality combines reading data from files, processing and calculating portfolio values,
storing data in an SQLite database, and generating a line plot using matplotlib.

"""

import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sqlite3
import portfolio

# Create a connection to the database
conn = sqlite3.connect('portfolio.db')

# Read the JSON file
try:
    with open('AllStocks.json') as json_file:
        stock_data = json.load(json_file)
except FileNotFoundError:
    print("Error: JSON file not found.")
    exit(1)
except json.JSONDecodeError:
    print("Error: Invalid JSON file format.")
    exit(1)

# Read the portfolio data
portfolio_data = portfolio.read_portfolio_data('Lesson6_Data_Stocks.csv')

# Extract the symbols from the portfolio data
portfolio_symbols = portfolio.get_portfolio_symbols(portfolio_data)

# Calculate portfolio values based on stock data
portfolio_values = {}
dates = set()


for stock in stock_data:
    symbol = stock['Symbol']
    date = datetime.strptime(stock['Date'], '%d-%b-%y').date()
    closing_price = stock['Close']
    shares = portfolio_data.get(symbol, {}).shares

    # Calculate the value of the stock based on shares and closing price
    stock_value = shares * closing_price

    # Store the stock value in the portfolio values dictionary
    if date not in portfolio_values:
        portfolio_values[date] = {}
    portfolio_values[date][symbol] = stock_value

    # Keep track of unique dates
    dates.add(date)

# Sort the dates in ascending order
sorted_dates = sorted(dates)

# Prepare the data for plotting
stock_values = {symbol: [] for symbol in portfolio_symbols}


# Create a table in the database
conn.execute("CREATE TABLE IF NOT EXISTS portfolio (date DATE, symbol TEXT, value FLOAT)")

for date in sorted_dates:
    for symbol in portfolio_symbols:
        value = portfolio_values.get(date, {}).get(symbol, 0)
        stock_values[symbol].append(value)

        # Insert the values into the database table
        conn.execute("INSERT INTO portfolio (date, symbol, value) VALUES (?, ?, ?)",
                     (date, symbol, value))

# Commit the changes to the database
conn.commit()

# Fill in missing values with zeros
for symbol in portfolio_symbols:
    missing_values = len(sorted_dates) - len(stock_values[symbol])
    stock_values[symbol].extend([0] * missing_values)

# Plot the stock values over time
fig, ax = plt.subplots(figsize=(10, 6))

for symbol in portfolio_symbols:
    ax.plot(sorted_dates, stock_values[symbol], label=symbol)

# Format the x-axis dates
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d, %Y'))
plt.xticks(rotation=45, ha='right')

plt.xlabel('Date')
plt.ylabel('Stock Value')
plt.title('Portfolio Value Over Time')
plt.legend()
plt.tight_layout()
plt.savefig('portfolio_graph.png')
plt.show()

# Close the database connection
conn.close()
