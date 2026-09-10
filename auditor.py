inventory = 0
failed_entries = 0

while True:
    stock = input("Enter stock quantity (or 'quit' to end): ")

    if stock.lower() == "quit":
            print("\n--- Inventory Report ---")
            print("Total Units Processed:", inventory)
            print("Number of Failed/Rejected Entries:", failed_entries)
            break
     
    if not stock.isdigit():
        print("Error: Invalid entries. Please enter a whole number.")
        failed_entries += 1
        continue

    stock = int(stock)

    if stock < 0:
        print("Error: Negative stock entries input are not allowed.")
        failed_entries += 1
        continue

    inventory += stock

    print("Stock has been successfully added.")
    print("Current inventory:", inventory)

    if inventory > 500:
        print("Warning: Inventory exceeds 500 units.")
        break


    

