/* eslint-disable @typescript-eslint/no-explicit-any */
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
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

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
  const sortedFiles = [...fileData]
    .sort((a, b) => b.tokens - a.tokens)
    .slice(0, 20);

  const labels = sortedFiles.map((file) => file.name);
  const data = sortedFiles.map((file) => file.tokens);

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
    <Card className="p-2">
      <CardHeader className="p-4">
        <CardTitle>Top 20 Files by Context Length</CardTitle>
      </CardHeader>
      <CardContent className="p-4">
        <div className="chart-container">
          <Bar data={chartData} options={chartOptions as any} />
        </div>
      </CardContent>
    </Card>
  );
}

export { TopFilesChart };
