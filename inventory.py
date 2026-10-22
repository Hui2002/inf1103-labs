from product import Product

class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        for existing_product in self.__products:
            if existing_product.get_id() == product.get_id():
                return False

        self.__products.append(product)
        return True

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_id() == product_id:
                return product

        return None

    def display_all(self):
        print("\nCurrent Inventory")
        print("------------------------------------------")

        if len(self.__products) == 0:
            print("No products found.")

        else:
            for product in self.__products:
                print(
                    f"ID: {product.get_id()} | "
                    f"Name: {product.get_name()} | "
                    f"Price: ${product.get_price():.2f} | "
                    f"Stock: {product.get_stock()}"
                )

        print("------------------------------------------")


    def get_products(self):
        return self.__products.copy()
