import os
import json

from product import Product
from inventory import Inventory

FILENAME = "inventory.json"

def load_inventory():
    inventory = Inventory()

    if os.path.exists(FILENAME):
        print("inventory.json found.")

        try:
            with open(FILENAME, "r") as file:
                data = json.load(file)

            for item in data:
                product = Product(
                    item["id"],
                    item["name"],
                    item["price"],
                    item["stock"]
                )

                if not inventory.add_product(product):
                    raise ValueError("Duplicate product ID in file.")

            print("Inventory loaded successfully.")
            return inventory

        except (OSError, ValueError, TypeError, KeyError):
            print("Error loading inventory.json.")
            return Inventory()

    else:
        print("inventory.json not found.")
        print("Starting with default inventory.")

        inventory.add_product(
            Product("P001", "Laptop", 1200.00, 15)
        )

        inventory.add_product(
            Product("P002", "Mouse", 25.50, 40)
        )

        inventory.add_product(
            Product("P003", "Keyboard", 45.00, 25)
        )

        return inventory


def save_inventory(inventory):
    data = []

    for product in inventory.get_products():
        product_data = {
            "id": product.get_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock()
        }

        data.append(product_data)

    try:
        with open(FILENAME, "w") as file:
            json.dump(data, file, indent=4)

        print("Inventory saved successfully to inventory.json.")

    except OSError:
        print("Error saving inventory.json.")
