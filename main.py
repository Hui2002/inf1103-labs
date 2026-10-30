from file_handler import load_inventory, save_inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from file_handler import load_inventory, save_inventory

def display_menu():
    print("\n---------- MENU ----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("--------------------------")



def add_product(inventory):
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")

    product_type = input("Select product type: ").strip()

    if product_type not in ("1", "2"):
        print("Invalid product type.")
        return

    product_id = input("Product ID: ").strip()
    product_name = input("Product Name: ").strip()

    if inventory.search_product(product_id) is not None:
        print("Product ID already exists.")
        return

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))

        if product_type == "1":
            weight = float(input("Weight (kg): "))

            product = PhysicalProduct(
                product_id,
                product_name,
                price,
                stock,
                weight
            )

        elif product_type == "2":
            download_size = float(input("Download Size (MB): "))

            product = DigitalProduct(
                product_id,
                product_name,
                price,
                stock,
                download_size
            )

        if inventory.add_product(product):
            print("\nProduct added successfully!")

    except ValueError as error:
        print(f"Invalid product details: {error}")



def update_stock(inventory):
    print("\nUpdate Stock")

    product_id = input("Enter Product ID: ")
    product = inventory.search_product(product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")

    try:
        new_stock = int(input("\nNew Stock Quantity: "))

        if product.update_stock(new_stock):
            print("\nStock updated successfully!")
        else:
            print("\nStock cannot be negative.")

    except ValueError:
        print("Invalid stock quantity.")

def search_product(inventory):
    print("\nSearch Product")

    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print("------------------------------------------")

    product.display_information()

    print("------------------------------------------")

def main():
    print("==========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("==========================================")
    
    inventory = load_inventory()

    while True:
        display_menu()

        option = input("\nEnter option: ")

        if option == "1":
            inventory.display_all()

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
            save_inventory(inventory)
            
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break

        else:
            print("\nInvalid option. Please select 1 to 6.")


if __name__ == "__main__":
    main()