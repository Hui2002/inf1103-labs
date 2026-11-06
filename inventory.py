from product import Product

class Inventory:

    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        # Prevent duplicate product IDs
        if self.find_product(product.get_id()) is not None:
            return False

        self.__products.append(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_id() == product_id:
                return product

        return None

    def search_product(self, product_id: str) -> Product | None:
        # Keep existing method for compatibility
        return self.find_product(product_id)

    def remove_product(self, product_id: str) -> bool:
        for index, product in enumerate(self.__products):
            if product.get_id() == product_id:
                self.__products.pop(index)
                return True

        return False

    def display_all(self) -> None:
        print("\nCurrent Inventory")

        if not self.__products:
            print("No products found.")
            return

        for product in self.__products:
            print("------------------------------------------")
            product.display_information()

        print("------------------------------------------")

    def get_products(self) -> list[Product]:
        return self.__products.copy()
