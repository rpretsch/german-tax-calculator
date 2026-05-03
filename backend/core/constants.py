"""This file contains all constants used in the tax/social deduction calculations."""

from dataclasses import dataclass


@dataclass
class CalculationConstants:
    """
    Constants to be used in the tax/social deduction calculations. Usually vary year-to-year.

    Attributes
    ----------
    pension_contribution_rate: float
        The rate of the total pension contribution to be paid from the gross salary.
    minijob_threshold: float
        The threshold of gross salary, upto which an employment counts as a Minijob. Employments in this range experience very small deductions.
    midijob_threshold: float
        The threshold of gross salary, upto which an employment counts as a Midijob. The lower boundary for this range is the `minijob_threshold`. Employments in this range experience small deductions, but larger ones than in a Minijob.
    midijob_factor_f: float
        The factor which is used for calculating the variable pension contributions in the Midijob range.
    salary_tax_rate: float  # TODO
        The salary tax rate
    church_tax_rate: float  # TODO
        The church tax rate
    """

    pension_contribution_rate: float
    minijob_threshold: float
    midijob_threshold: float
    midijob_factor_f: float
    salary_tax_rate: float  # TODO
    church_tax_rate: float  # TODO


@dataclass
class UserSettings:
    """
    Individual settings to be set by the user.

    Attributes
    ----------
    is_voluntarily_pension_insured: bool
        If the user pays voluntary pension deductions in a Minijob.
    is_employed_in_household: bool
        If the user is employed in a private household
    """

    is_voluntarily_pension_insured: bool
    is_employed_in_household: bool


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
