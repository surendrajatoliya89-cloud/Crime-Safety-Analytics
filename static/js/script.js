// CrimeWatch Analytics - Chart.js Visualizations with Multi-Year & Geographical Analysis
document.addEventListener("DOMContentLoaded", function () {
  if (!document.getElementById("crimeTypeChart") && !document.getElementById("cityChart") && !document.getElementById("stateChart") && !document.getElementById("yearlyTrendChart")) {
    return;
  }

  fetch("/api/charts-data")
    .then((response) => response.json())
    .then((data) => {
      // 0. Yearly Trend Line Chart (2021-2024)
      if (document.getElementById("yearlyTrendChart") && data.year_counts) {
        new Chart(document.getElementById("yearlyTrendChart"), {
          type: "line",
          data: {
            labels: Object.keys(data.year_counts),
            datasets: [
              {
                label: "Total Incidents per Year",
                data: Object.values(data.year_counts),
                borderColor: "rgba(37, 99, 235, 1)",
                backgroundColor: "rgba(37, 99, 235, 0.15)",
                fill: true,
                tension: 0.3,
                pointRadius: 6,
                pointBackgroundColor: "rgba(37, 99, 235, 1)",
                borderWidth: 2,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true, grid: { color: "#f1f5f9" } } },
          },
        });
      }

      // 0A. State Comparison Bar Chart
      if (document.getElementById("stateChart") && data.state_counts) {
        new Chart(document.getElementById("stateChart"), {
          type: "bar",
          data: {
            labels: Object.keys(data.state_counts),
            datasets: [
              {
                label: "Incidents by State",
                data: Object.values(data.state_counts),
                backgroundColor: "rgba(14, 116, 144, 0.8)",
                borderColor: "rgba(14, 116, 144, 1)",
                borderWidth: 1,
                borderRadius: 4,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true, grid: { color: "#f1f5f9" } } },
          },
        });
      }

      // 0B. City Comparison Bar Chart
      if (document.getElementById("cityChart") && data.city_counts) {
        new Chart(document.getElementById("cityChart"), {
          type: "bar",
          data: {
            labels: Object.keys(data.city_counts),
            datasets: [
              {
                label: "Reported Incidents",
                data: Object.values(data.city_counts),
                backgroundColor: "rgba(30, 58, 138, 0.8)",
                borderColor: "rgba(30, 58, 138, 1)",
                borderWidth: 1,
                borderRadius: 4,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true, grid: { color: "#f1f5f9" } } },
          },
        });
      }

      // 1. Crime by Type Bar Chart
      if (document.getElementById("crimeTypeChart")) {
        new Chart(document.getElementById("crimeTypeChart"), {
          type: "bar",
          data: {
            labels: Object.keys(data.crime_types),
            datasets: [
              {
                label: "Reported Incidents",
                data: Object.values(data.crime_types),
                backgroundColor: "rgba(16, 185, 129, 0.75)",
                borderColor: "rgba(5, 150, 105, 1)",
                borderWidth: 1,
                borderRadius: 4,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true, grid: { color: "#f1f5f9" } } },
          },
        });
      }

      // 2. Crime Trend Line Chart (Monthly Seasonality)
      if (document.getElementById("crimeTrendChart")) {
        new Chart(document.getElementById("crimeTrendChart"), {
          type: "line",
          data: {
            labels: Object.keys(data.monthly_trends),
            datasets: [
              {
                label: "Incidents per Month",
                data: Object.values(data.monthly_trends),
                borderColor: "rgba(245, 158, 11, 1)",
                backgroundColor: "rgba(245, 158, 11, 0.1)",
                tension: 0.3,
                fill: true,
                pointRadius: 4,
                pointBackgroundColor: "rgba(245, 158, 11, 1)",
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true, grid: { color: "#f1f5f9" } } },
          },
        });
      }

      // 5. Severity Distribution Doughnut Chart
      if (document.getElementById("severityChart")) {
        new Chart(document.getElementById("severityChart"), {
          type: "doughnut",
          data: {
            labels: Object.keys(data.severity_counts),
            datasets: [
              {
                data: Object.values(data.severity_counts),
                backgroundColor: [
                  "rgba(34, 197, 94, 0.8)",  // Low
                  "rgba(234, 179, 8, 0.8)",  // Medium
                  "rgba(239, 68, 68, 0.8)",  // High
                ],
                borderWidth: 1,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { position: "bottom" },
            },
          },
        });
      }
    })
    .catch((error) => console.error("Error loading charts data:", error));
});
