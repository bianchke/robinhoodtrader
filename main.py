import robin_stocks as r
import pandas as pd
import numpy as np
from ta import *

def get_last_crossing(df, days, symbol="", direction=""):
    """Searches for a crossing between two indicators for a given stock
    Args:
        df(pandas.core.frame.DataFrame): Pandas dataframe with columns containing the stock's prices, both indicators, and the dates
        days(int): Specifies the maximum number of days that the cross can occur by
        symbol(str): Symbol of the stock we're querying. Optional, used for printing purposes
        direction(str): "above" if we are searching for an upwards cross, "below" if we are searching for a downwaords cross. Optional, used for printing purposes
    Returns:
        1 if the short-term indicator crosses above the long-term one
        0 if there is no cross between the indicators
        -1 if the short-term indicator crosses below the long-term one
    """
    prices = df.loc[:,"Price"]
    shortTerm = df.loc[:,"Indicator1"]
    LongTerm = df.loc[:,"Indicator2"]
    dates = df.loc[:,"Dates"]
    lastIndex = prices.size - 1
    index = lastIndex
    found = index
    recentDiff = (shortTerm.at[index] - LongTerm.at[index]) >= 0
    if((direction == "above" and not recentDiff) or (direction == "below" and recentDiff)):
        return 0
    index -= 1
    while(index >= 0 and found == lastIndex and not np.isnan(shortTerm.at[index]) and not np.isnan(LongTerm.at[index]) \
                        and ((pd.Timestamp("now", tz='UTC') - dates.at[index]) <= pd.Timedelta(str(days) + " days"))):
        if(recentDiff):
            if((shortTerm.at[index] - LongTerm.at[index]) < 0):
                found = index
        else:
            if((shortTerm.at[index] - LongTerm.at[index]) > 0):
                found = index
        index -= 1
    if(found != lastIndex):
        if((direction == "above" and recentDiff) or (direction == "below" and not recentDiff)):
            print(symbol + ": Short SMA crossed" + (" ABOVE " if recentDiff else " BELOW ") + "Long SMA at " + str(dates.at[found]) \
                +", which was " + str(pd.Timestamp("now", tz='UTC') - dates.at[found]) + " ago", ", price at cross: " + str(prices.at[found]) \
                + ", current price: " + str(prices.at[lastIndex]))
        return (1 if recentDiff else -1)
    else:
        return 0

def golden_cross(stockTicker, n1, n2, days, direction=""):
    """Determine if a golden/death cross has occured for a specified stock in the last X trading days
    Args:
        stockTicker(str): Symbol of the stock we're querying
        n1(int): Specifies the short-term indicator as an X-day moving average.
        n2(int): Specifies the long-term indicator as an X-day moving average.
                 (n1 should be smaller than n2 to produce meaningful results, e.g n1=50, n2=200)
        days(int): Specifies the maximum number of days that the cross can occur by
        direction(str): "above" if we are searching for an upwards cross, "below" if we are searching for a downwaords cross. Optional, used for printing purposes
    Returns:
        1 if the short-term indicator crosses above the long-term one
        0 if there is no cross between the indicators
        -1 if the short-term indicator crosses below the long-term one
        False if direction == "above" and five_year_check(stockTicker) returns False, meaning that we're considering whether to
            buy the stock but it hasn't risen overall in the last five years, suggesting it contains fundamental issues
    """
    #if(direction == "above" and not five_year_check(stockTicker)):
    #    return False

    history = r.get_historicals(stockTicker,span='year',bounds='regular')
    closingPrices = []
    dates = []
    for item in history:
        closingPrices.append(float(item['close_price']))
        dates.append(item['begins_at'])
    price = pd.Series(closingPrices)
    dates = pd.Series(dates)
    dates = pd.to_datetime(dates)
    sma1 = volatility.bollinger_mavg(price, n=int(n1), fillna=False)
    sma2 = volatility.bollinger_mavg(price, n=int(n2), fillna=False)
    series = [price.rename("Price"), sma1.rename("Indicator1"), sma2.rename("Indicator2"), dates.rename("Dates")]
    df = pd.concat(series, axis=1)
    cross = get_last_crossing(df, days, symbol=stockTicker, direction=direction)

    return cross


r.login('bianchke@lemoyne.edu', 'Holimont3!')

# build_holdings() compiles all stocks into a dict
my_stocks = r.build_holdings()

for key, value in my_stocks.items():
	print(key, value)

print('Would you like to buy a stock? (Y/N)')
answer = input()
if answer.lower() == "y":
	print("Enter Symbol")
	symbol = input()
	symbol = symbol.upper()
	print("Enter Quantity")
	quantity = input()
	if quantity.isdigit():
		print('Buy', quantity, 'shares of', symbol, 'Stock? (Y/N)')
		answer = input()
		if answer.lower() == 'y':
			r.order_buy_market(symbol, quantity)
else:
	example = golden_cross('GOOGL', 50, 200, 10, "Above")
	print(example)

