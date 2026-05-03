document
  .getElementById("tax-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const year = document.getElementById("year").value;
    const gross_salary = document.getElementById("gross_salary").value;

    fetch("/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ year: year, gross_salary: gross_salary }),
    })
      .then((response) => response.json())
      .then((data) => {
        document.getElementById("result").textContent =
          "Take-home pay:" + data.result + "€";
      });
  });
