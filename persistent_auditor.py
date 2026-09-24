def get_valid_input(failed_attempts_tracker):
    """Handles prompt, input validation, and returns an integer or 'quit' signal."""
    while True:
        user_input = input("Enter stock quantity (or 'quit' to end): ").strip()
        
        if user_input.lower() == "quit":
            return "quit", failed_attempts_tracker
        
        if user_input.isdigit():
            return int(user_input), failed_attempts_tracker
        else:
            print("Error: Invalid entry. Please enter a whole positive number.")
            failed_attempts_tracker += 1


def process_delivery(current_total, new_value):
    """Calculates and returns the updated running total."""
    return current_total + new_value


def calculate_tax(amount):
    """Calculates 10% tax for a specific delivery amount."""
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    """Prints the final summary report."""
    print("\n--- Inventory Report ---")
    print("Total Units Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)


def main():
    inventory = 0
    failed_entries = 0

    while True:
        entry, failed_entries = get_valid_input(failed_entries)

        if entry == "quit":
            generate_report(inventory, failed_entries)
            break

        # Valid input processed through functions
        inventory = process_delivery(inventory, entry)
        tax = calculate_tax(entry)

        print("Stock has been successfully added.")
        print(f"Tax for this delivery (10%): {tax:.2f}")
        print("Current inventory:", inventory)

        if inventory > 500:
            print("\nWarning: Inventory exceeds 500 units.")
            generate_report(inventory, failed_entries)
            break


if __name__ == "__main__":
    main()