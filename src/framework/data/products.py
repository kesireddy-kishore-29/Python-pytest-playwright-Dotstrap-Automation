"""Sauce Demo's catalogue, as the shop publishes it. Same names and prices as the UI flagship."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Product:
    name: str
    price: Decimal


PRODUCTS = {
    "backpack": Product("Sauce Labs Backpack", Decimal("29.99")),
    "bike_light": Product("Sauce Labs Bike Light", Decimal("9.99")),
    "bolt_t_shirt": Product("Sauce Labs Bolt T-Shirt", Decimal("15.99")),
    "fleece_jacket": Product("Sauce Labs Fleece Jacket", Decimal("49.99")),
    "onesie": Product("Sauce Labs Onesie", Decimal("7.99")),
    "red_t_shirt": Product("Test.allTheThings() T-Shirt (Red)", Decimal("15.99")),
}
