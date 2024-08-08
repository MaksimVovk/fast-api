# Write a Python program that can do the following:

# - You have $50

# - You buy an item that is $15, that has a 3% tax

# - Using the print()  Print how much money you have left, after purchasing the item.

bank = 50
itemPrice = 15
taxCof = .03
tax = itemPrice * taxCof
price = itemPrice + tax
leftAmount = bank - price

print(f'bank: ${bank}')
print(f'tax: ${tax}')
print(f'price with tax: ${price}')
print(f'left amount: ${leftAmount}')
