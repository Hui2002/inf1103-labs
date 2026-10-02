import os
import json

def load_inventory():
    if os.path.exists("inventory.json"):
        print("inventory.json found.")

        try:
            with open("inventory.json", "r") as file:
                inventory = json.load(file)

            print("Inventory loaded successfully.")
            return inventory

        except:
            print("Error loading inventory.json.")
            return []

    else:
        print("inventory.json not found.")
        print("Starting with default inventory.")

        inventory = [
            {
                "id": "P001",
                "name": "Laptop",
                "price": 1200.00,
                "stock": 15
            },
            {
                "id": "P002",
                "name": "Mouse",
                "price": 25.50,
                "stock": 40
            },
            {
                "id": "P003",
                "name": "Keyboard",
                "price": 45.00,
                "stock": 25
            }
        ]

        return inventory
