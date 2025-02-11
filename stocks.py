# Name: Jonah Taylor
# Student ID: 2626247
# Resources: Used some online resources to understand API concepts
#            and the basics of storing dictionaries in json files 


# Importing the needed libraries
import requests as r
from datetime import date
import json
from sys import argv

# The header needed to access the API without issue (the user-agent is pulled from my PC)
header = {'user-agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0'}

def download_data(ticker: str) -> dict:
    """ A function that pulls raw historical data about a stock (given its ticker symbol) from the past 5 years and stores it in a dictionary. """

    ticker = ticker.upper()
    today = date.today()
    start = str(today.replace(year=today.year - 5))
    base_url = "https://api.nasdaq.com"
    path = f"/api/quote/{ticker}/historical?assetclass=stocks&fromdate={start}&limit=9999"
    # combining the base url (NASDAQ API) and the specific path
    full_url = base_url + path
    response = r.get(full_url, headers = header)

    # API error handling
    # 200 is the successful response code
    if response.status_code == 200:
        try:
            data = response.json()
            # Returning the raw data in the form of a dict
            return data
        # If any other status code is produced, program exits
        except ValueError:
            print("There was an error in producing the data.")


def data_processing(Stock_dict:dict) -> list:
    """ A function that processes a stock's raw API data (given a ticker symbol) into a list of its historic closing prices (last 5 years of data). """

    # Sorting through the three keys in the data dict
    rows = Stock_dict['data']['tradesTable']['rows']
    # Iterating through the "rows" key to isolate the closing prices
    closing_prices = []
    for row in rows:
        close_price = row.get('close', None)
        closing_prices.append(float(close_price.replace('$','')))

    # Returning a list of a stocks closing prices
    return closing_prices



def stock_analysis(prices: list) -> dict:
    """ A function that produces statistical analysis of a stock's closing price given its ticker symbol. """
    
    # Calculating basic statistical measures of a stock's closing prices
    max_price = max(prices)
    min_price = min(prices)
    avg_price = sum(prices) / len(prices)
    sorted_price = sorted(prices)
    middle_price = len(prices) // 2

    # Ff the length is divisable by 2, the mean of the 2 sorted middle values is returned as the median price
    if len(sorted_price) % 2 != 0:
        median_price = sorted_price[middle_price]
    else:
        median_price = (sorted_price[middle_price-1] + sorted_price[middle_price]) / 2
    
    # A dictionary of this statistical information (found in json)
    return {
        "min": min_price,
        "max": max_price,
        "avg": avg_price,
        "median": median_price,
        "ticker": ticker
    }

# Looping through arguments (tickers) and producing a json with stock stats
tickers = argv[1:]
results = []

for ticker in tickers:
    results.append(stock_analysis(data_processing(download_data(ticker))))

f = open("stocks.json", 'w')

json.dump(results, f, indent = 4)

f.close()