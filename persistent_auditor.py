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