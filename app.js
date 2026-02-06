let ctx = document.getElementById("categoryChart").getContext("2d");
let chart;

// Load & update chart
function updateChart() {
    fetch("/data")
        .then(res => res.json())
        .then(data => {
            document.querySelector("h3").innerText =
                `Total Spent: $${data.total.toFixed(2)}`;

            if (!chart) {
                chart = new Chart(ctx, {
                    type: "bar",
                    data: {
                        labels: Object.keys(data.category_totals),
                        datasets: [{
                            label: "Spending by Category ($)",
                            data: Object.values(data.category_totals),
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: { y: { beginAtZero: true } }
                    }
                });
            } else {
                chart.data.labels = Object.keys(data.category_totals);
                chart.data.datasets[0].data = Object.values(data.category_totals);
                chart.update();
            }
        });
}

// Save edit
document.querySelectorAll(".save-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        const id = btn.dataset.id;
        const amount = document.querySelector(`.edit-amount[data-id='${id}']`).value;
        const category = document.querySelector(`.edit-category[data-id='${id}']`).value;

        fetch(`/update/${id}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ amount, category })
        }).then(() => updateChart());
    });
});

// Delete one
document.querySelectorAll(".delete-btn").forEach(btn => {
    btn.addEventListener("click", e => {
        e.preventDefault();
        fetch(btn.href).then(() => {
            btn.closest("tr").remove();
            updateChart();
        });
    });
});

// Delete all
document.querySelector(".delete-all").addEventListener("click", e => {
    e.preventDefault();
    fetch("/delete_all").then(() => {
        document.querySelectorAll("tbody tr").forEach(tr => tr.remove());
        updateChart();
    });
});

updateChart();
