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

        if not self.__products:
            print("No product found")
            return

        for product in self.__products:
            print("------------------------------------------")
            product.display_information()
            
        print("------------------------------------------")



    def get_products(self):
        return self.__products.copy()
