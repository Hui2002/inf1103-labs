import os

INVENTORY_FILE = "inventory.txt"
ORDERS_FILE = "orders.txt"

def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        return 0, []

    try:
        with open(INVENTORY_FILE, "r") as file:
            lines = [line.strip() for line in file if line.strip()]

            total = int(lines[0]) if len(lines) > 0 and lines[0].isdigit() else 0

            history = []
            if len(lines) > 1 and lines[1]:
                history = [
                    int(val.strip())
                    for val in lines[1].split(",")
                    if val.strip().isdigit()
                ]

            return total, history
    except (ValueError, IOError):
        return 0, []

def save_inventory(total_units, history_list):
    try:
        with open(INVENTORY_FILE, "w") as file:
            file.write(f"{total_units}\n")
            file.write(",".join(str(val) for val in history_list) + "\n")
        print(f"Inventory data successfully saved to {INVENTORY_FILE}")
    except IOError as e:
        print(f"Error saving inventory file: {e}")

def load_orders():
    orders = []
    if os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE, "r") as file:
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

    if not orders:
        orders = [
            (1001, "Wireless Mouse", 2),
            (1002, "Keyboard", 1),
            (1003, "USB Cable", 3),
        ]
    return orders

def save_orders(orders):
    """Saves all structured order records to orders.txt."""
    try:
        with open(ORDERS_FILE, "w") as file:
            for order_id, product_name, quantity in orders:
                file.write(f"{order_id},{product_name},{quantity}\n")
        print(f"Order successfully saved to {ORDERS_FILE}")
    except IOError as e:
        print(f"Error saving orders file: {e}") 

def display_orders(orders):
    """Prints the current active orders matching requirement formatting."""
    print("Current Orders:\n")
    if not orders:
        print("No existing orders found.\n")
    else:
        for order_id, product_name, quantity in orders:
            print(f"{order_id}, {product_name}, {quantity}")
        print()


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10


def generate_report(total_units, failed_attempts, history, orders):
    print("\n--- Inventory Report ---")
    print("Total Units Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)
    print("Quantity History List:", history)
    print("\nAll Logged Orders:")
    for order_id, product_name, quantity in orders:
        print(f"  ID: {order_id} | Product: {product_name} | Quantity: {quantity}")


def get_valid_input(failed_attempts_tracker, next_id):
    """Collects input for Product Name & Quantity, or handles 'quit' signal."""
    product_name = input("Enter Product Name (or 'quit' to end): ").strip()

    if product_name.lower() == "quit":
        return "quit", None, failed_attempts_tracker

    while True:
        quantity_input = input("Enter Quantity: ").strip()

        if quantity_input.lower() == "quit":
            return "quit", None, failed_attempts_tracker

        if quantity_input.isdigit() and int(quantity_input) > 0:
            quantity = int(quantity_input)
            return product_name, quantity, failed_attempts_tracker
        else:
            print("Error: Invalid entry. Please enter a whole positive number.")
            failed_attempts_tracker += 1

def main():
    # 1. Load initial state
    inventory, transaction_history = load_inventory()
    orders = load_orders()
    failed_entries = 0

    # Display loaded orders
    display_orders(orders)

    while True:
        next_id = 1001 if not orders else max(order[0] for order in orders) + 1

        product_name, quantity, failed_entries = get_valid_input(failed_entries, next_id)

        # Check for quit signal
        if product_name == "quit":
            generate_report(inventory, failed_entries, transaction_history, orders)
            save_inventory(inventory, transaction_history)
            save_orders(orders)
            break

        # 2. Track Order History
        new_order = (next_id, product_name, quantity)
        orders.append(new_order)
        transaction_history.append(quantity)

        # Calculate values
        inventory = process_delivery(inventory, quantity)
        tax = calculate_tax(quantity)

        print("\nNew Order Added:")
        print(f"{new_order[0]},{new_order[1]},{new_order[2]}")
        print(f"Tax for this delivery (10%): {tax:.2f}")
        print("Current inventory total:", inventory)

        # Save updates to orders.txt
        save_orders(orders)
        print()

        # Check max capacity threshold
        if inventory > 500:
            print("\nWarning: Inventory exceeds 500 units.")
            generate_report(inventory, failed_entries, transaction_history, orders)
            save_inventory(inventory, transaction_history)
            save_orders(orders)
            break


if __name__ == "__main__":
    main()