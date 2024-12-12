import React from "react";
import { Bar } from "react-chartjs-2";


interface TopFilesChartParams {
    labels: string[];
    data: number[];
}

function formatNumber(number: number) {
    return number.toLocaleString();
}

const TopFilesChart: React.FC<TopFilesChartParams> = ({ labels, data }) => {
  const chartData = {
    labels: labels,
    datasets: [
      {
        label: "Context Length",
        data: data,
        backgroundColor: "#36A2EB",
        borderColor: "#2693e6",
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: function (context: any) {
            return `${formatNumber(context.raw)} tokens`;
          },
        },
      },
    },
    scales: {
      x: {
        title: { display: true, text: "File Names" },
        ticks: {
          autoSkip: false,
          maxRotation: 45,
          minRotation: 45,
        },
      },
      y: {
        title: { display: true, text: "Context Length" },
        ticks: { beginAtZero: true },
      },
    },
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <h2 className="text-xl font-semibold mb-4">
        Top 20 Files by Context Length
      </h2>
      <div className="chart-container">
        <Bar data={chartData} options={chartOptions as any} />
      </div>
    </div>
  );
};

export default TopFilesChart;