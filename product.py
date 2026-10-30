from abc import ABC, abstractmethod

class Product(ABC):

    @abstractmethod
    def get_fulfilment_info(self):
        pass
    
    def __init__(self, product_id, name, price, stock):
        if price < 0:
            raise ValueError("Price cannot be negative.")

        if stock < 0:
            raise ValueError("Stock cannot be negative.")

        self.__id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def update_stock(self, new_stock):
        if new_stock < 0:
            return False

        self.__stock = new_stock
        return True

    def display_information(self):
        print(f"ID: {self.__id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
