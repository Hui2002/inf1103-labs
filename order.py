from product import Product
from order_line import OrderLine

class Order:
    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def add_order_line(
        self, product: Product, quantity: int
    ) -> None:
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def get_order_lines(self) -> tuple[OrderLine, ...]:
        return tuple(self.__order_lines)

    def remove_order_line(self, product_id: str) -> bool:
        for index, line in enumerate(self.__order_lines):
            if line.product.get_id() == product_id:
                self.__order_lines.pop(index)
                return True

        return False

    def calculate_total(self) -> float:
        total = 0.0

        for line in self.__order_lines:
            total += line.calculate_subtotal()

        return total
