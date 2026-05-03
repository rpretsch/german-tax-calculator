"""This file contains all the calcualtion logic for taxes and social security deductions."""

from .constants import CalculationConstants


class Pension:
    """
    Calculates pension insurance contributions for a given year.

    Attributes
    ----------
    year: int
        The year used for the calcuations. Used to retrieve the correct constants valid for that year.
    calculation_constants: CalculationConstants
        Constants for the given year used in calculations.
    """

    calculation_constants: CalculationConstants

    def __init__(
        self, year: int, calculation_constants: dict[int, CalculationConstants]
    ) -> None:

        self.year = year
        self.calculation_constants = calculation_constants[self.year]

    def calculate_total_pension_gross_salary(self, gross_salary: float) -> float:
        """
        Calculates the virtual gross salary used for the total pension insurance contribution calculations.
        Source: § 20 Abs. 2a SGB IV

        Parameters
        ----------
        gross_salary : float
            The gross_salary of the employee.

        Returns
        -------
        float
            The pension gross salary used for the total pension insurance contributions.
            Rounded to the nearest cent.
        """

        minijob_threshold = self.calculation_constants.minijob_threshold
        midijob_threshold = self.calculation_constants.midijob_threshold
        midijob_factor_f = self.calculation_constants.midijob_factor_f

        result = round(
            midijob_factor_f * minijob_threshold
            + (
                midijob_threshold / (midijob_threshold - minijob_threshold)
                - minijob_threshold
                / (midijob_threshold - minijob_threshold)
                * midijob_factor_f
            )
            * (gross_salary - minijob_threshold),
            2,
        )

        return result

    def calculate_employee_pension_gross_salary(self, gross_salary: float) -> float:
        """
        Calculates the virtual gross salary used for the employee pension insurance contribution calculations.
        Source: § 20 Abs. 2a SGB IV

        Parameters
        ----------
        gross_salary : float
            The gross_salary of the employee.

        Returns
        -------
        float
            The pension gross salary used for the total pension insurance contributions.
            Rounded to the nearest cent.
        """

        minijob_threshold = self.calculation_constants.minijob_threshold
        midijob_threshold = self.calculation_constants.midijob_threshold

        result = round(
            midijob_threshold
            / (midijob_threshold - minijob_threshold)
            * (gross_salary - minijob_threshold),
            2,
        )

        return result

    def calculate_total_contribution(self, gross_salary: float) -> float:
        """
        Calculates the total pension contributions.
        Source: § 2 Abs. 1 BVV

        Paramters
        ---------
        gross_salary : float
            The gross salary of the employee.

        Returns
        -------
        float
            The total pension contributions.
            Rounded to the nearest cent.
        """

        pension_contribution_rate = self.calculation_constants.pension_contribution_rate
        total_pension_gross_salary = self.calculate_total_pension_gross_salary(
            gross_salary
        )

        result = round(
            round(total_pension_gross_salary * pension_contribution_rate / 2.0, 2)
            * 2.0,
            2,
        )

        return result

    def calculate_employee_contribution(self, gross_salary: float) -> float:
        """
        Calculates the employee pension contributions.
        Source: § 2 Abs. 2 BVV

        Paramters
        ---------
        gross_salary : float
            The gross salary of the employee.

        Returns
        -------
        float
            The employee pension contributions.
            Rounded to the nearest cent.
        """

        pension_contribution_rate = self.calculation_constants.pension_contribution_rate
        employee_pension_gross_salary = self.calculate_employee_pension_gross_salary(
            gross_salary
        )

        result = round(
            employee_pension_gross_salary * pension_contribution_rate / 2.0, 2
        )

        return result

    def calculate_employer_contribution(self, gross_salary: float) -> float:
        """
        Calculates the employer pension contributions.
        Source: § 2 Abs. 2 BVV

        Paramters
        ---------
        gross_salary : float
            The gross salary of the employee.

        Returns
        -------
        float
            The employer pension contributions.
            Rounded to the nearest cent.
        """

        total_contribution = self.calculate_total_contribution(gross_salary)
        employee_contribution = self.calculate_employer_contribution(gross_salary)

        result = round(total_contribution - employee_contribution, 2)

        return result
