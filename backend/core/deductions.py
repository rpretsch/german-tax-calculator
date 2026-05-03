"""This file contains all the calcualtion logic for taxes and social security deductions."""

from .constants import CalculationConstants, UserSettings


class Tax:
    """
    Calculates the taxes for a given year.

    Attributes
    ----------
    year: int
        The year used for the calcuations. Used to retrieve the correct constants valid for that year.
    calculation_constants: CalculationConstants
        Constants for the given year used in calculations.
    user_settings: UserSettings
        Individual settings also affecting the calculations.
    """

    year: int
    calculation_constants: CalculationConstants
    user_settings: UserSettings

    def __init__(
        self,
        year: int,
        calculation_constants: dict[int, CalculationConstants],
        user_settings: UserSettings,
    ) -> None:

        self.year = year
        self.calculation_constants = calculation_constants[self.year]
        self.user_settings = user_settings

    def calculate_salary_tax(self, gross_salary: float) -> float:
        """
        Calculates the salary tax.
        Source: ...

        Parameters
        ----------
        gross_salary : float
            The gross_salary of the employee.

        Returns
        -------
        float
            The salary tax.
            Rounded to the nearest cent.
        """

        salary_tax_rate = self.calculation_constants.salary_tax_rate

        result = round(gross_salary * salary_tax_rate, 2)

        return result

    def calculate_church_tax(self, gross_salary: float) -> float:
        """
        Calculates the church tax.
        Source: ...

        Parameters
        ----------
        gross_salary : float
            The gross_salary of the employee.

        Returns
        -------
        float
            The church tax.
            Rounded to the nearest cent.
        """

        church_tax_rate = self.calculation_constants.church_tax_rate

        result = round(gross_salary * church_tax_rate, 2)

        return result


class Pension:
    """
    Calculates pension insurance contributions for a given year.

    Attributes
    ----------
    year: int
        The year used for the calcuations. Used to retrieve the correct constants valid for that year.
    calculation_constants: CalculationConstants
        Constants for the given year used in calculations.
    user_settings: UserSettings
        Individual settings also affecting the calculations.
    """

    calculation_constants: CalculationConstants

    def __init__(
        self,
        year: int,
        calculation_constants: dict[int, CalculationConstants],
        user_settings: UserSettings,
    ) -> None:

        self.year = year
        self.calculation_constants = calculation_constants[self.year]
        self.user_settings = user_settings

    def calculate_employee_contribution(self, gross_salary: float) -> float:
        """
        Calculates the employee pension contributions.

        Parameters
        ----------
        gross_salary : float
            The gross salary of the employee.

        Returns
        -------
        float
            The employee pension contributions.
            Rounded to the nearest cent.
        """

        pension_contribution_rate = self.calculation_constants.pension_contribution_rate
        minijob_threshold = self.calculation_constants.minijob_threshold

        # § 20 Abs. 2a SGB IV - Virtual gross salary for the pension deduction calculations in a Midijob
        # § 168 Abs. 1 SGB VI - Employee and employer each pay half of the total pension contribution
        if gross_salary > minijob_threshold:
            employee_pension_gross_salary = (
                self._calculate_employee_pension_gross_salary(gross_salary)
            )

            result = round(
                employee_pension_gross_salary * pension_contribution_rate / 2.0, 2
            )

        else:
            is_voluntarily_pension_insured = (
                self.user_settings.is_voluntarily_pension_insured
            )

            # § 6 Abs. 1b SGB VI - Voluntary pension insurance in a Minijob
            if is_voluntarily_pension_insured:
                is_employed_in_household = self.user_settings.is_employed_in_household

                # § 168 Abs. 1 SGB VI - Different pension contribution rate if employer is a private household
                if is_employed_in_household:
                    employer_contribution_rate = 0.05

                else:
                    employer_contribution_rate = 0.15

                employee_contribution_rate = (
                    pension_contribution_rate - employer_contribution_rate
                )

                # § 163 Abs. 8 SGB VI - Minimum baseline for pension contribution calculations. As the employer pays a flat rate, the difference has to be paid by the employee
                if gross_salary > 175.0:
                    result = round(gross_salary * employee_contribution_rate, 2)

                else:
                    total_contributions = self._calculate_total_contribution(
                        175.0
                    )
                    employer_contributions = (
                        self.calculate_employer_contribution(gross_salary)
                    )
                    result = round(
                        total_contributions - employer_contributions, 2
                    )

            else:
                result = 0.0

        return result

    def calculate_employer_contribution(self, gross_salary: float) -> float:
        """
        Calculates the employer pension contributions.
        Source: § 2 Abs. 2 BVV

        Parameters
        ----------
        gross_salary : float
            The gross salary of the employee.

        Returns
        -------
        float
            The employer pension contributions.
            Rounded to the nearest cent.
        """

        minijob_threshold = self.calculation_constants.minijob_threshold

        # § 168 Abs. 1 SGB VI - Different pension contribution rate for an employer with an employee in a Minijob
        if gross_salary > minijob_threshold:
            total_contribution = self._calculate_total_contribution(gross_salary)
            employee_contribution = self.calculate_employee_contribution(gross_salary)

            result = round(total_contribution - employee_contribution, 2)

        else:
            is_employed_in_household = self.user_settings.is_employed_in_household

            # § 168 Abs. 1 SGB VI - Different pension contribution rate for if employer is a private household
            if is_employed_in_household:
                employer_pension_contribution_rate = 0.05

            else:
                employer_pension_contribution_rate = 0.15

            result = round(gross_salary * employer_pension_contribution_rate, 2)

        return result

    def _calculate_total_pension_gross_salary(self, gross_salary: float) -> float:
        """
        Calculates the virtual gross salary used for the total pension insurance contribution calculations in a Midijob.
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

    def _calculate_employee_pension_gross_salary(self, gross_salary: float) -> float:
        """
        Calculates the virtual gross salary used for the employee pension insurance contribution calculations in a Midijob.
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

    def _calculate_total_contribution(self, gross_salary: float) -> float:
        """
        Calculates the total pension contributions.

        Parameters
        ----------
        gross_salary : float
            The gross salary of the employee.

        Returns
        -------
        float
            The total pension contributions.
            Rounded to the nearest cent.
        """

        pension_contribution_rate = self.calculation_constants.pension_contribution_rate
        total_pension_gross_salary = self._calculate_total_pension_gross_salary(
            gross_salary
        )

        result = round(
            round(total_pension_gross_salary * pension_contribution_rate / 2.0, 2)
            * 2.0,
            2,
        )  # § 2 Abs. 1 BVV - The value has to be halved, rounded and then doubled again

        return result
