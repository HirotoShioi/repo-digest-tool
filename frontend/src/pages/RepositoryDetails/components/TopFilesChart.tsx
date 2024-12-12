import { FileData } from "@/types";
import { formatNumber } from "@/utils/formatters";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

// 必要な構成要素を登録
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface TopFilesChartParams {
    fileData: FileData[];
}

function TopFilesChart({ fileData }: TopFilesChartParams) {

    // Sort fileData by tokens in descending order and take top 20
    const sortedFiles = [...fileData].sort((a, b) => b.tokens - a.tokens).slice(0,20);


    const labels = sortedFiles.map(file => file.name);
    const data = sortedFiles.map(file => file.tokens);

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