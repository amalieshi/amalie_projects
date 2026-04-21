"""Data generator for creating test product data."""

import json
import random
import uuid
from pathlib import Path
from typing import Dict, List, Any

from config import PRODUCT_DATA_FILE


class ProductDataGenerator:
    """Generates realistic test data for product testing."""

    def __init__(self):
        self.load_templates()

    def load_templates(self):
        """Load product templates from JSON file."""
        with open(PRODUCT_DATA_FILE, "r") as f:
            data = json.load(f)

        self.templates = data["product_templates"]
        self.categories = data["product_categories"]
        self.adjectives = data["name_adjectives"]
        self.colors = data["name_colors"]
        self.sizes = data["name_sizes"]

    def generate_random_product(self) -> Dict[str, Any]:
        """Generate a single random product."""
        template = random.choice(self.templates)

        # Generate variations of the base name
        name_variations = [
            template["name"],
            f"{random.choice(self.adjectives)} {template['name']}",
            f"{random.choice(self.colors)} {template['name']}",
            f"{template['name']} - {random.choice(self.sizes)}",
            f"{random.choice(self.adjectives)} {random.choice(self.colors)} {template['name']}",
        ]

        # Generate SKU with random identifier
        random_id = str(uuid.uuid4())[:8].upper()
        sku = template["sku"].format(random_id=random_id)

        # Generate price within range
        price_min, price_max = template["price_range"]
        price = round(random.uniform(price_min, price_max), 2)

        # Generate quantity within range
        qty_min, qty_max = template["quantity_range"]
        quantity = random.randint(qty_min, qty_max)

        return {
            "name": random.choice(name_variations),
            "sku": sku,
            "price": price,
            "quantity": quantity,
            "category": template["category"],
        }

    def generate_product_batch(self, count: int) -> List[Dict[str, Any]]:
        """Generate a batch of random products."""
        products = []
        used_skus = set()

        for _ in range(count):
            attempts = 0
            while attempts < 10:  # Prevent infinite loop
                product = self.generate_random_product()

                # Ensure unique SKU
                if product["sku"] not in used_skus:
                    products.append(product)
                    used_skus.add(product["sku"])
                    break

                attempts += 1

        return products

    def generate_performance_test_data(self, count: int = 100) -> List[Dict[str, Any]]:
        """Generate data specifically for performance testing."""
        return self.generate_product_batch(count)

    def save_generated_data(self, products: List[Dict[str, Any]], filename: str):
        """Save generated products to JSON file."""
        output_path = Path(__file__).parent / "test_oracles" / filename
        with open(output_path, "w") as f:
            json.dump(products, f, indent=2)

    def get_test_categories(self) -> List[str]:
        """Get list of available categories for testing."""
        return self.categories.copy()


if __name__ == "__main__":
    # Generate sample data for testing
    generator = ProductDataGenerator()

    # Generate 100 products for performance testing
    perf_products = generator.generate_performance_test_data(100)
    generator.save_generated_data(perf_products, "performance_test_products.json")
    print(f"Generated {len(perf_products)} products for performance testing")

    # Generate 20 products for general testing
    test_products = generator.generate_product_batch(20)
    generator.save_generated_data(test_products, "general_test_products.json")
    print(f"Generated {len(test_products)} products for general testing")
