import robin_stocks as rs 

rs.login('ENTER USERNAME', 'ENTER PASSWORD')

# build_holdings() compiles all stocks into a dict
my_stocks = rs.build_holdings()

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
			rs.order_buy_market(symbol, quantity)
