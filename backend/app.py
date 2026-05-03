import os
import logging
from flask import Flask, jsonify, request, send_from_directory
from core import Pension, calculation_constants

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__, static_folder=os.path.join(BASE_DIR, "frontend"), static_url_path=""
)


@app.route("/")
def index():
    return send_from_directory(os.path.join(BASE_DIR, "frontend"), "main.html")


@app.route("/calculate", methods=["POST"])
def calculate():

    data = request.get_json()

    gross_salary = float(data.get("gross_salary", 0))
    year = int(data.get("year", 2026))

    logging.debug("Running request for %d %.2f", year, gross_salary)

    pension = Pension(year, calculation_constants)
    employee_pension_contribution = pension.calculate_employee_contribution(
        gross_salary
    )

    logging.debug("Employee pension contribution: %.2f", employee_pension_contribution)

    result = round(gross_salary - employee_pension_contribution, 2)

    logging.debug("Result: %.2f", result)

    return jsonify({"result": result})


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
