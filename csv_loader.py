import csv

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier


def load_products(
    path: str,
    inventory: Inventory,
    supplier: Supplier
) -> None:

    try:
        file = open(path, newline="", encoding="utf-8-sig")

    except FileNotFoundError:
        print(f"Products file not found: {path}")

    else:
        loaded = 0

        with file:
            reader = csv.reader(file)

            # Skip CSV header
            next(reader, None)

            for row_number, row in enumerate(reader, start=2):

                try:
                    # Validate number of columns
                    if len(row) != 5:
                        raise ValueError(
                            "Expected 5 columns."
                        )

                    (
                        product_type,
                        product_id,
                        name,
                        price,
                        stock_quantity
                    ) = [value.strip() for value in row]

                    product_type = product_type.lower()

                    # Use ProductFactory to create products
                    product = ProductFactory.create(
                        product_type,
                        product_id,
                        name,
                        float(price),
                        int(stock_quantity),
                        supplier,
                        weight=(0.0 if product_type == "physical"else None),
                        download_size=(0.0 if product_type == "digital"else None)
                    )

                    if not inventory.add_product(product):
                        raise ValueError(
                            f"Duplicate product ID: {product_id}"
                        )

                    loaded += 1

                except ValueError as error:
                    print(f"Skipping row {row_number}: {error}")

        print(f"{loaded} products loaded.")

    finally:
        print("Load attempt finished.")
