from product import Product
from can_be_shipped import CanBeShipped

class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)

        if weight < 0:
            raise ValueError("Weight cannot be negative.")

        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight} kg")

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        return self.__weight * 5.0

CanBeShipped.register(PhysicalProduct)