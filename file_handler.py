import os
import json

from supplier import Supplier
from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

FILENAME = "inventory.json"

def load_inventory() -> Inventory:
    inventory = Inventory()

    # Create default products if no JSON file exists
    if not os.path.exists(FILENAME):
        supplier = Supplier("UNKNOWN", "Unassigned", "")

        inventory.add_product(
            PhysicalProduct("P001", "Laptop", 1200.00, 15, 0.0, supplier)
        )
        inventory.add_product(
            PhysicalProduct("P002", "Mouse", 25.50, 40, 0.0, supplier)
        )
        inventory.add_product(
            PhysicalProduct("P003", "Keyboard", 45.00, 25, 0.0, supplier)
        )

        return inventory

    with open(FILENAME, "r") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("Inventory JSON must contain a list.")

    # Reuse Supplier objects with the same supplier ID
    suppliers: dict[str, Supplier] = {}

    for item in data:
        product_type = item.get("type", "physical").strip().lower()

        # Support older Lab 7 records without supplier details
        supplier_data = item.get("supplier")

        if supplier_data is None:
            supplier_data = {
                "supplier_id": "UNKNOWN",
                "name": "Unassigned",
                "contact_email": ""
            }

        supplier_id = supplier_data["supplier_id"]

        if supplier_id not in suppliers:
            suppliers[supplier_id] = Supplier(
                supplier_id,
                supplier_data["name"],
                supplier_data["contact_email"]
            )

        supplier = suppliers[supplier_id]

        if product_type == "physical":
            product = PhysicalProduct(
                item["id"],
                item["name"],
                item["price"],
                item["stock"],
                item.get("weight", 0.0),
                supplier
            )

        elif product_type == "digital":
            product = DigitalProduct(
                item["id"],
                item["name"],
                item["price"],
                item["stock"],
                item["download_size"],
                supplier
            )

        else:
            raise ValueError(
                f"Unknown product type: {product_type}"
            )

        if not inventory.add_product(product):
            raise ValueError("Duplicate product ID in JSON.")

    return inventory


def save_inventory(inventory: Inventory) -> bool:
    data = []

    for product in inventory.get_products():
        supplier = product.get_supplier()

        product_data = {
            "id": product.get_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock(),
            "supplier": {
                "supplier_id": supplier.get_supplier_id(),
                "name": supplier.get_name(),
                "contact_email": supplier.get_contact_email()
            }
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

        print("Inventory saved successfully.")
        return True

    except OSError as error:
        print(f"Error saving inventory: {error}")
        return False
