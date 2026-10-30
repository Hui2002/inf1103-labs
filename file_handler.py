import os
import json

from product import Product
from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

FILENAME = "inventory.json"

def load_inventory():
    inventory = Inventory()

    if not os.path.exists(FILENAME):
        print("inventory.json not found.")
        print("Starting with default inventory.")

        inventory.add_product(
            PhysicalProduct("P001", "Laptop", 1200.00, 15, 0.0)
        )
        inventory.add_product(
            PhysicalProduct("P002", "Mouse", 25.50, 40, 0.0)
        )
        inventory.add_product(
            PhysicalProduct("P003", "Keyboard", 45.00, 25, 0.0)
        )

        return inventory
    try:
        with open(FILENAME, "r") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Inventory JSON must contain a list.")

        for item in data:
            product_type = item.get("type", "physical")

            if product_type == "physical":
                if "type" not in item or "weight" not in item:
                    print(
                        f"Note: {item['id']} has no saved weight. "
                        "Using 0.0 kg temporarily."
                    )

                product = PhysicalProduct(
                    item["id"],
                    item["name"],
                    item["price"],
                    item["stock"],
                    item.get("weight", 0.0)
                )
            
            elif product_type == 'digital':
                product = DigitalProduct(
                    item["id"],
                    item["name"],
                    item["price"],
                    item["stock"],
                    item["download_size"]
                )
            else:
                raise ValueError(
                    f"Unknown product type: {product_type}"
                )

            if not inventory.add_product(product):
                raise ValueError("Duplicate product ID in JSON.")

        print("Inventory loaded successfully.")
        return inventory

    except (OSError, ValueError, TypeError, KeyError) as error:
        print(f"Error loading inventory: {error}")
        raise


def save_inventory(inventory):
    data = []

    for product in inventory.get_products():
        product_data = {
            "id": product.get_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock()
        }

        if isinstance(product, PhysicalProduct):
            product_data["type"] = "physical"
            product_data["weight"] = product.get_weight()

        elif isinstance(product, DigitalProduct):
            product_data["type"] = "digital"
            product_data["download_size"] = product.get_download_size()

        else:
            raise ValueError("Unsupported product type.")

        data.append(product_data)

    try:
        with open(FILENAME, "w") as file:
            json.dump(data, file, indent=4)

        print("Inventory saved successfully to inventory.json.")
        return True

    except OSError:
        print(f"Error saving inventory: {error}")
        return False
