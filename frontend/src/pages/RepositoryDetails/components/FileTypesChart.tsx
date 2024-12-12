import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

type FileTypeAggregation = {
  extension: string;
  count: number;
  tokens: number;
};

interface FileTypesChartParams {
  fileTypes: FileTypeAggregation[];
}

function FileTypesChart({ fileTypes }: FileTypesChartParams) {
  // tokens (context length) で降順ソート
  const sortedFileTypes = [...fileTypes].sort((a, b) => b.tokens - a.tokens);

  const labels = sortedFileTypes.map((fileType) => fileType.extension);
  const data = sortedFileTypes.map((fileType) => fileType.tokens);

  const chartData = {
    labels: labels,
    datasets: [
      {
        data: data,
        backgroundColor: [
          "#FF6384",
          "#36A2EB",
          "#FFCE56",
          "#4BC0C0",
          "#9966FF",
          "#FF9F40",
          "#FF6384",
          "#36A2EB",
          "#FFCE56",
          "#4BC0C0",
        ],
      },
    ],
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <h2 className="text-xl font-semibold">
        Context length distribution by file type
      </h2>
      <span className="text-sm text-gray-500 block">
        (Total context length for each file type, sorted by size)
      </span>
      <div className="chart-container">
        <Pie data={chartData} />
      </div>
    </div>
  );
}

export default FileTypesChart;
