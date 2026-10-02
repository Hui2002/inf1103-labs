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
                "price": 1200.0,
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

def save_inventory(inventory):
    with open("inventory.json", "w") as file:
        json.dump(inventory, file, indent=4)

    print("Inventory saved successfully to inventory.json.")


def display_all(inventory):
    print("\nCurrent Inventory")
    print("------------------------------------------")

    if len(inventory) == 0:
        print("No products found.")

    else:
        for product in inventory:
            print(
                f"ID: {product['id']} | "
                f"Name: {product['name']} | "
                f"Price: ${product['price']:.2f} | "
                f"Stock: {product['stock']}"
            )

    print("------------------------------------------")

def add_product(inventory):
    print("\nAdd New Product")

    product_id = input("Product ID: ")
    product_name = input("Product Name: ")

    # Check whether ID already exists
    for product in inventory:
        if product["id"] == product_id:
            print("Product ID already exists.")
            return

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))

        new_product = {
            "id": product_id,
            "name": product_name,
            "price": price,
            "stock": stock
        }

        inventory.append(new_product)

        print("\nProduct added successfully!")

    except ValueError:
        print("Invalid price or stock quantity.")

def update_stock(inventory):
    print("\nUpdate Stock")

    product_id = input("Enter Product ID: ")

    for product in inventory:

        if product["id"] == product_id:

            print("\nProduct Found:")
            print(f"Name: {product['name']}")
            print(f"Current Stock: {product['stock']}")

            try:
                new_stock = int(input("\nNew Stock Quantity: "))

                product["stock"] = new_stock

                print("\nStock updated successfully!")

            except ValueError:
                print("Invalid stock quantity.")

            return

    print("\nProduct not found.")

def search_product(inventory):
    print("\nSearch Product")

    product_id = input("Enter Product ID: ")

    for product in inventory:

        if product["id"] == product_id:

            print("\nProduct Found")
            print("------------------------------------------")
            print(f"ID: {product['id']}")
            print(f"Name: {product['name']}")
            print(f"Price: ${product['price']:.2f}")
            print(f"Stock: {product['stock']}")
            print("------------------------------------------")

            return

    print("\nProduct not found.")

def display_menu():
    print("\n---------- MENU ----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("--------------------------")

def main():

    print("==========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("==========================================\n")

    inventory = load_inventory()

    while True:

        display_menu()

        option = input("\nEnter option: ")

        if option == "1":
            display_all(inventory)

        elif option == "2":
            add_product(inventory)

        elif option == "3":
            update_stock(inventory)

        elif option == "4":
            search_product(inventory)

        elif option == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)

        elif option == "6":

            print("\nSaving inventory before exit...")

            with open("inventory.json", "w") as file:
                json.dump(inventory, file, indent=4)

            print("Inventory saved successfully.")

            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")

            break

        else:
            print("\nInvalid option. Please select 1 to 6.")


main()
