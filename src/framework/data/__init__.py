"""Test data: factories with unique, sweepable names, and the demo shop's catalogue."""

from framework.data.factories import a_booking, a_customer, unique_email, unique_name
from framework.data.products import PRODUCTS, Product

__all__ = ["PRODUCTS", "Product", "a_booking", "a_customer", "unique_email", "unique_name"]
