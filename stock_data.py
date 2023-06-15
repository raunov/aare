import requests
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

def modules(symbol, module):
    """
    Fetches financial data for a given symbol and a list of modules.

    Args:
        symbol (str): A single stock ticker representing the stock.
        module (str): A comma-separated list of the types of financial data to fetch. Must include one or more of the following:
            - asset-profile
            - income-statement
            - balance-sheet
            - cashflow-statement
            - default-key-statistics
            - calendar-events
            - sec-filings
            - upgrade-downgrade-history
            - institution-ownership
            - fund-ownership
            - insider-transactions
            - insider-holders
            - earnings-history

    Returns:
        dict: A dictionary containing the requested financial data.
    """
    url = "https://mboum-finance.p.rapidapi.com/mo/module/"
    querystring = {"symbol": symbol, "module": module}
    headers = {
        "X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY") ,
        "X-RapidAPI-Host": "mboum-finance.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()
# modules("LHV1T.TL", "asset-profile,default-key-statistics")

def news(symbol):
    """
    Fetches the latest news for a given stock symbol from the MBoum Finance API.

    Args:
        symbol (str): The stock symbol to fetch news for.

    Returns:
        dict: A dictionary containing the JSON response with the news data.
    """
    url = "https://mboum-finance.p.rapidapi.com/ne/news/"
    querystring = {"symbol": symbol}
    headers = {
        "X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY") ,
        "X-RapidAPI-Host": "mboum-finance.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()
# news("EGR1T.TL")

def quotes(symbol):
    url = "https://mboum-finance.p.rapidapi.com/qu/quote"
    querystring = {"symbol": symbol}
    headers = {
        "X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY") ,
        "X-RapidAPI-Host": "mboum-finance.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()
# quotes("TSLA")