import os
from flask import Flask, jsonify, request, send_from_directory
from core import calculate_tax

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
    income = float(data.get("income", 0))
    result = calculate_tax(income)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
