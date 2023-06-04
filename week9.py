import pandas as pd

# Define the stock symbols and the SPY symbol
symbols = ['AIG', 'F', 'FB', 'GOOG', 'IBM', 'MSFT', 'RDS-A', 'SPY']

# Create an empty dictionary to store the dataframes for each stock
stock_dataframes = {}

# Import data into pandas DataFrames
for symbol in symbols:
    filename = symbol + '.csv'
    try:
        df = pd.read_csv(filename, parse_dates=['Date'])
        stock_dataframes[symbol] = df
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")

# Calculate average stock price and standard deviation for each stock
for symbol, df in stock_dataframes.items():
    avg_price = df['Close'].mean()
    std_dev = df['Close'].std()
    print(f"Stock: {symbol}, Average Price: {avg_price:.2f}, Standard Deviation: {std_dev:.2f}")

# Compute correlation coefficient with SPY for each stock
spy_df = stock_dataframes['SPY']
for symbol, df in stock_dataframes.items():
    correlation = df['Close'].corr(spy_df['Close'])
    print(f"Stock: {symbol}, Correlation with SPY: {correlation:.2f}")

# Plot stock prices over time
import matplotlib.pyplot as plt

for symbol, df in stock_dataframes.items():
    plt.plot(df['Date'], df['Close'], label=symbol)

plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.title('Stock Prices Over Time')
plt.legend()
plt.show()
