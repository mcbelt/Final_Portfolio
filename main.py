"""
Author:         Mauricio Beltran
Date:           06/04/2023
Functionality:

Overall, this code retrieves portfolio and stock data, performs data preprocessing,
calculates daily and cumulative returns, and visualizes the cumulative returns of 
the stocks in the portfolio over time.

"""

import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import portfolio


try:
    # Create a connection to the database
    conn = sqlite3.connect('portfolio.db')

    # Read the portfolio data
    portfolio_data = portfolio.read_portfolio_data('Lesson6_Data_Stocks.csv')

    # Get the symbols from the portfolio
    portfolio_symbols = portfolio.get_portfolio_symbols(portfolio_data)

    # Read stock data from the database into a Pandas DataFrame
    df = pd.read_sql_query("SELECT * FROM portfolio", conn)

    # Convert the 'date' column to datetime type
    df['date'] = pd.to_datetime(df['date'])

    # Handle duplicate entries by aggregating the values using the mean
    df = df.groupby(['date', 'symbol']).mean().reset_index()

    # Pivot the DataFrame to have symbols as columns and dates as rows
    pivot_df = df.pivot(index='date', columns='symbol', values='value')

    # Calculate the daily returns of each stock
    returns_df = pivot_df.pct_change()

    # Calculate the cumulative returns of each stock
    cumulative_returns_df = (1 + returns_df).cumprod()

    # Plot the cumulative returns of each stock
    cumulative_returns_df.plot(figsize=(10, 6))
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.title('Cumulative Returns of Portfolio Stocks')
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Close the database connection
    conn.close()

except FileNotFoundError:
    print("Error: File not found.")
except pd.errors.EmptyDataError:
    print("Error: Empty data.")
except sqlite3.Error as e:
    print("Error: SQLite database error -", str(e))
except Exception as e:
    print("Error:", str(e))
