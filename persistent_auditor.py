import os

FILENAME = "inventory.txt"


def load_inventory():
    """Reads saved order records from inventory.txt if present."""
    orders = []
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        parts = line.split(",")
                        if len(parts) == 3:
                            order_id = int(parts[0].strip())
                            product_name = parts[1].strip()
                            quantity = int(parts[2].strip())
                            orders.append((order_id, product_name, quantity))
        except (ValueError, IOError):
            orders = []
    return orders


def save_inventory(orders):
    """Saves all order records to inventory.txt."""
    try:
        with open(FILENAME, "w") as file:
            for order_id, product_name, quantity in orders:
                file.write(f"{order_id},{product_name},{quantity}\n")
        print("Order successfully saved to inventory.txt")
    except IOError as e:
        print(f"Error saving to file: {e}")


def display_orders(orders):
    """Displays current loaded orders matching the exact terminal output format."""
    print("Current Orders:")
    if not orders:
        print("  (No previous orders found)")
    else:
        for order_id, product_name, quantity in orders:
            print(f"  {order_id}, {product_name}, {quantity}")
    print()


def calculate_tax(amount):
    """Calculates 10% tax based on $0.10 per unit."""
    return amount * 0.10


def generate_report(orders, failed_attempts):
    """Prints the === Audit Report === section matching the image exactly."""
    total_transactions = len(orders)
    total_units = sum(order[2] for order in orders)

    print("\n=== Audit Report ===")
    print(f"Total Transactions Recorded: {total_transactions}")
    print(f"Total Units Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def main():
    orders = load_inventory()
    display_orders(orders)

    failed_entries = 0

    while True:
        product_name = input("Enter Product Name (or 'quit' to exit): ").strip()

        if product_name.lower() == "quit":
            save_inventory(orders)
            generate_report(orders, failed_entries)
            break

        # Input validation for quantity
        while True:
            quantity_input = input("Enter Quantity: ").strip()
            
            if quantity_input.lower() == "quit":
                save_inventory(orders)
                generate_report(orders, failed_entries)
                return

            if quantity_input.isdigit() and int(quantity_input) > 0:
                quantity = int(quantity_input)
                break
            else:
                print("Error: Invalid entry. Please enter a whole positive number.")
                failed_entries += 1

        # Calculate next Order ID starting at 1001
        next_id = 1001 if not orders else max(order[0] for order in orders) + 1
        new_order = (next_id, product_name, quantity)
        orders.append(new_order)

        # Output formatting matching image
        tax = calculate_tax(quantity)
        total_inventory = sum(order[2] for order in orders)

        print("\nNew Order Added:")
        print(f"{new_order[0]}, {new_order[1]}, {new_order[2]}")
        print(f"Tax: ${tax:.2f} | Total Inventory: {total_inventory}\n")


if __name__ == "__main__":
    main()