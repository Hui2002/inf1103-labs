import unittest
import tempfile
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from supplier import Supplier
from product_factory import ProductFactory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from discount_strategy import (
    NoDiscount,
    PercentageDiscount,
    BulkDiscount,
    StudentDiscount
)
from order import Order
from order_line import OrderLine
from inventory import Inventory
from csv_loader import load_products
from main import get_positive_float

# 1. STRATEGY PATTERN TESTS
class TestStrategyPattern(unittest.TestCase):

    def setUp(self) -> None:
        supplier = Supplier(
            "S001", "Tech Supplies",
            "contact@example.com"
        )

        product = ProductFactory.create(
            "physical", "P001", "Guitar",
            125.0, 10, supplier, weight=2.5
        )

        self.order = Order("ORD001")
        self.order.add_order_line(product, 2)

    def test_no_discount(self):
        self.assertEqual(
            self.order.calculate_total(), 250.0
        )

    def test_percentage_discount(self):
        self.order.set_discount(PercentageDiscount(10))
        self.assertEqual(
            self.order.calculate_total(), 225.0
        )

    def test_bulk_discount(self):
        self.order.set_discount(BulkDiscount(200, 20))
        self.assertEqual(
            self.order.calculate_total(), 230.0
        )

    def test_bulk_discount_below_threshold(self):
        self.order.set_discount(BulkDiscount(300, 20))
        self.assertEqual(
            self.order.calculate_total(), 250.0
        )

    def test_student_discount(self):
        self.order.set_discount(StudentDiscount())
        self.assertEqual(
            self.order.calculate_total(), 237.5
        )

    def test_switch_strategy(self):
        self.order.set_discount(BulkDiscount(200, 20))
        self.assertEqual(
            self.order.calculate_total(), 230.0
        )

        self.order.set_discount(PercentageDiscount(10))
        self.assertEqual(
            self.order.calculate_total(), 225.0
        )

    def test_invalid_discount_percentage(self):
        with self.assertRaises(ValueError):
            PercentageDiscount(150)

# 2. FACTORY PATTERN TESTS
class TestFactoryPattern(unittest.TestCase):

    def setUp(self) -> None:
        self.supplier = Supplier(
            "S001", "Tech Supplies",
            "contact@example.com"
        )

    def test_create_physical_product(self):
        product = ProductFactory.create(
            "physical", "P001", "Monitor",
            250.0, 10, self.supplier, weight=4.5
        )

        self.assertIsInstance(product, PhysicalProduct)
        self.assertIs(product.get_supplier(), self.supplier)

    def test_create_digital_product(self):
        product = ProductFactory.create(
            "digital", "D001", "Software",
            50.0, 20, self.supplier,
            download_size=500
        )

        self.assertIsInstance(product, DigitalProduct)
        self.assertIs(product.get_supplier(), self.supplier)

    def test_unknown_product_type(self):
        with self.assertRaisesRegex(
            ValueError, "Unknown product type"
        ):
            ProductFactory.create(
                "service", "S001", "Installation",
                30.0, 5, self.supplier
            )

    def test_missing_physical_weight(self):
        with self.assertRaises(ValueError):
            ProductFactory.create(
                "physical", "P002", "Keyboard",
                50.0, 10, self.supplier
            )

# 3. VALIDATION TESTS
class TestValidation(unittest.TestCase):

    def setUp(self) -> None:
        self.supplier = Supplier(
            "S001", "Tech Supplies",
            "contact@example.com"
        )

        self.product = ProductFactory.create(
            "physical", "P001", "Monitor",
            250.0, 10, self.supplier, weight=4.5
        )

    def test_invalid_price(self):
        for price in (0, -10):
            with self.subTest(price=price):
                with self.assertRaises(ValueError):
                    ProductFactory.create(
                        "physical", "P002", "Mouse",
                        price, 10, self.supplier,
                        weight=0.5
                    )

    def test_negative_stock(self):
        for product_type, extra in (
            ("physical", {"weight": 1.0}),
            ("digital", {"download_size": 500})
        ):
            with self.subTest(product_type=product_type):
                with self.assertRaises(ValueError):
                    ProductFactory.create(
                        product_type, "P003", "Item",
                        50.0, -5, self.supplier, **extra
                    )

    def test_invalid_order_quantity(self):
        for quantity in (0, -3):
            with self.subTest(quantity=quantity):
                with self.assertRaises(ValueError):
                    OrderLine(self.product, quantity)

    def test_negative_stock_update(self):
        with self.assertRaises(ValueError):
            self.product.update_stock(-5)


# 4. USER INPUT EXCEPTION HANDLING
class TestExceptionHandling(unittest.TestCase):

    def test_positive_float_input(self):
        with patch(
            "builtins.input",
            side_effect=["abc", "-5", "12.50"]
        ):
            with patch("sys.stdout", new_callable=StringIO) as output:
                result = get_positive_float("Price: ")

        self.assertEqual(result, 12.5)
        self.assertIn(
            "Please enter a valid number",
            output.getvalue()
        )
        self.assertIn(
            "Please enter a number greater than zero",
            output.getvalue()
        )


# 5. CSV LOADING TESTS
class TestCSVLoading(unittest.TestCase):

    def setUp(self) -> None:
        self.supplier = Supplier(
            "S001", "Tech Supplies",
            "contact@example.com"
        )
        self.inventory = Inventory()

    def test_csv_valid_and_invalid_rows(self):
        csv_content = (
            "product_type,product_id,name,price,stock_quantity\n"
            "physical,P001,Desk Lamp,25.00,10\n"
            "digital,D001,Photo Editor,49.90,100\n"
            "service,S001,Installation,30.00,5\n"
            "physical,P002,Office Chair,abc,3\n"
            "physical,P003,Monitor Stand,39.50,7\n"
        )

        with tempfile.TemporaryDirectory() as directory:
            csv_path = Path(directory) / "products.csv"
            csv_path.write_text(
                csv_content, encoding="utf-8"
            )

            with patch(
                "sys.stdout", new_callable=StringIO
            ) as output:
                load_products(
                    str(csv_path),
                    self.inventory,
                    self.supplier
                )

        self.assertEqual(
            len(self.inventory.get_products()), 3
        )

        for product_id in ("P001", "D001", "P003"):
            self.assertIsNotNone(
                self.inventory.find_product(product_id)
            )

        self.assertIsNone(
            self.inventory.find_product("P002")
        )

        self.assertIn(
            "Skipping row 4", output.getvalue()
        )
        self.assertIn(
            "Skipping row 5", output.getvalue()
        )
        self.assertIn(
            "3 products loaded.", output.getvalue()
        )
        self.assertIn(
            "Load attempt finished.", output.getvalue()
        )

    def test_missing_csv_file(self):
        with tempfile.TemporaryDirectory() as directory:
            missing_path = Path(directory) / "missing.csv"

            with patch(
                "sys.stdout", new_callable=StringIO
            ) as output:
                load_products(
                    str(missing_path),
                    self.inventory,
                    self.supplier
                )

        self.assertEqual(
            len(self.inventory.get_products()), 0
        )
        self.assertIn(
            "Products file not found", output.getvalue()
        )
        self.assertIn(
            "Load attempt finished.", output.getvalue()
        )


if __name__ == "__main__":
    unittest.main()
