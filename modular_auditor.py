def get_valid_input():
    """Handles prompt, input validation, and returns an integer or 'quit' signal."""
    while True:
        user_input = input("Enter stock quantity (or 'quit' to end): ")
        
        if user_input.lower() == "quit":
            return "quit"
        
        if user_input.isdigit():
            return int(user_input)
        else:
            print("Error: Invalid entry. Please enter a whole positive number.")
            return None  