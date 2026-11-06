from abc import ABC, abstractmethod
from supplier import Supplier

class Product(ABC):

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass
    

    def __init__(self,product_id: str,name: str,price: float,stock: int,supplier: Supplier) -> None:

        if price < 0:
            raise ValueError("Price cannot be negative.")

        if stock < 0:
            raise ValueError("Stock cannot be negative.")

        self.__id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.__supplier: Supplier = supplier

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def get_id(self) -> str:
        return self.__id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def update_stock(self, new_stock: int) -> bool:
        if new_stock < 0:
            return False

        self.__stock = new_stock
        return True

    def display_information(self) -> None:
        print(f"ID: {self.__id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")

    
