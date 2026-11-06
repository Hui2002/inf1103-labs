
from product import Product
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from test_lsp import show_product_details


def test_polymorphism() -> None:
    supplier = Supplier(
        "S001", "Tech Supplies", "contact@example.com"
    )

    guitar = PhysicalProduct(
        "P101", "Guitar", 500.00, 10, 2.5, supplier
    )

    software = DigitalProduct(
        "D201", "Antivirus", 79.90, 100, 1500, supplier
    )

    inventory = Inventory()

    products: list[Product] = [guitar, software]

    # Add both subclasses through the Product type
    for product in products:
        assert inventory.add_product(product)

    print("\n--- Inventory Product Details ---")

    # Same method calls for every Product
    for product in inventory.get_products():
        print("--------------------------------")
        show_product_details(product)

    # Verify that each subclass provides its own behaviour
    fulfilment_info = [
        product.get_fulfilment_info()
        for product in inventory.get_products()
    ]

    assert len(fulfilment_info) == 2
    assert "physical shipping" in fulfilment_info[0].lower()
    assert "delivered digitally" in fulfilment_info[1].lower()

    print("\nALL POLYMORPHISM TESTS PASSED")


if __name__ == "__main__":
    test_polymorphism()
