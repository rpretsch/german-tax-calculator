"""This file contains all the calcualtion logic for taxes and social security deductions."""


def calculate_tax(income: float) -> dict[str, float]:
    # Placeholder: flat 20%
    tax = round(income * 0.20, 2)
    return {"tax": tax}
