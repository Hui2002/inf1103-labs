from product import Product
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


def test_lsp() -> None:
    supplier = Supplier(
        "S001", "Tech Supplies", "contact@example.com"
    )

    guitar = PhysicalProduct(
        "P101", "Guitar", 500.00, 10, 2.5, supplier
    )

    software = DigitalProduct(
        "D201", "Antivirus", 79.90, 100, 1500, supplier
    )

    products: list[Product] = [guitar, software]

    for product in products:
        print("\n--------------------------")
        show_product_details(product)

        # Both subclasses must support stock updates
        original_stock = product.get_stock()

        assert product.update_stock(20) is True
        assert product.get_stock() == 20

        # Negative stock should be rejected
        assert product.update_stock(-5) is False
        assert product.get_stock() == 20

        # Restore original stock
        assert product.update_stock(original_stock) is True

    print("\nALL LSP TESTS PASSED")


if __name__ == "__main__":
    test_lsp()
