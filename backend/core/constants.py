"""This file contains all constants used in the tax/social deduction calculations."""

from dataclasses import dataclass


@dataclass
class CalculationConstants:
    pension_contribution_rate: float
    minijob_threshold: float
    midijob_threshold: float
    midijob_factor_f: float
    salary_tax_rate: float  # TODO
    church_tax_rate: float  # TODO


calculation_constants = {
    2026: CalculationConstants(
        pension_contribution_rate=0.186,
        minijob_threshold=603.01,
        midijob_threshold=2000.0,
        midijob_factor_f=0.6619,
        salary_tax_rate=0.2,  # TODO
        church_tax_rate=0.05,  # TODO
    )
}
