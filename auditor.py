inventory = 0
failed_entries = 0

while True:
    stock = input("Enter stock quantity (or 'quit' to end): ")

    # Stop when user types quit
    if stock.lower() == "quit":
        break