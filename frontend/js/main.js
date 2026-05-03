document
  .getElementById("tax-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const is_voluntarily_pension_insured = document.getElementById(
      "is_voluntarily_pension_insured",
    ).checked;
    const is_employed_in_household = document.getElementById(
      "is_employed_in_household",
    ).checked;

    const year = document.getElementById("year").value;
    const gross_salary = document.getElementById("gross_salary").value;

    fetch("/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        year: year,
        gross_salary: gross_salary,
        is_voluntarily_pension_insured: is_voluntarily_pension_insured,
        is_employed_in_household: is_employed_in_household,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        document.getElementById("result").textContent =
          "Take-home pay: " + data.result + "€";
      });
  });
