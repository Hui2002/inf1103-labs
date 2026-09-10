inventory = 0
failed_entries = 0

while True:
    stock = input("Enter stock quantity (or 'quit' to end): ")

    if stock.lower() == "quit":
        break