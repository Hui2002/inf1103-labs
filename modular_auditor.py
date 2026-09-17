def get_valid_input():
    """Handles prompt, input validation, and returns an integer or 'quit' signal."""
    while True:
        user_input = input("Enter stock quantity (or 'quit' to end): ")
        
        if user_input.lower() == "quit":
            return "quit"
        
        if user_input.isdigit():
            return int(user_input)
        else:
            print("Error: Invalid entry. Please enter a whole positive number.1")
            return None  

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