import csv
from datetime import datetime
import json

class Investment:
    def __init__(self, symbol, shares, purchase_price, current_price, purchase_date):
        """
        Represents an investment holding with symbol, shares, purchase price, current price, and purchase date.
        """
        self.symbol = symbol
        self.shares = shares
        self.purchase_price = purchase_price
        self.current_price = current_price
        self.purchase_date = purchase_date

class Investor:
    """
    Investor class to store investor details
    """
    def __init__(self, investor_id, name, address, phone_number):
        self.investor_id = investor_id
        self.name = name
        self.address = address
        self.phone_number = phone_number

def read_portfolio_data(csv_file_path):
    """
    Reads the portfolio data from a CSV file and returns a dictionary of investments.
    """
    portfolio = {}
    try:
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                symbol = row['SYMBOL']
                shares = int(row['NO_SHARES'])
                purchase_price = float(row['PURCHASE_PRICE'])
                current_price = float(row['CURRENT_VALUE'])
                purchase_date = datetime.strptime(row['PURCHASE_DATE'], '%m/%d/%Y').date()

                investment = Investment(symbol, shares, purchase_price, current_price, purchase_date)
                portfolio[symbol] = investment
    except FileNotFoundError:
        print("Error: Portfolio data file not found.")
    except:
        print("Error: An unexpected error occurred while reading portfolio data.")
    return portfolio

def read_stocks_data(json_file_path):
    """
    Reads the stock data from a JSON file and returns a list of dictionaries representing stocks.
    """
    stocks = []
    try:
        with open(json_file_path) as json_file:
            stock_data = json.load(json_file)
            for stock in stock_data:
                symbol = stock['Symbol']
                date = datetime.strptime(stock['Date'], '%d-%b-%y').strftime('%Y-%m-%d')
                closing_price = float(stock['Close'])
                shares = stock.get('Shares', 0)

                stocks.append({'symbol': symbol, 'date': date, 'closing_price': closing_price, 'shares': shares})

    except FileNotFoundError:
        print("Error: Stock data file not found.")
    except:
        print("Error: An unexpected error occurred while reading stock data.")

    return stocks

def get_portfolio_symbols(portfolio):
    """
    Returns a list of symbols in the portfolio.
    """
    return portfolio.keys()
