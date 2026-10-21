"""Reads an amount out of display text: "$29.99", "Item total: $83.97", "Tax: $6.72"."""

import re
from decimal import Decimal

_AMOUNT = re.compile(r"\$([0-9]+(?:\.[0-9]{2})?)")


def money(text: str) -> Decimal:
    match = _AMOUNT.search(text)
    if match is None:
        raise ValueError(f'No amount in "{text}"')
    return Decimal(match.group(1))
