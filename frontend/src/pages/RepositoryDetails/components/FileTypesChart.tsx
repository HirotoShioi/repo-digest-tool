import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  TooltipItem,
} from "chart.js";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  CardDescription,
} from "@/components/ui/card";

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
  const sortedFileTypes = [...fileTypes].sort((a, b) => b.tokens - a.tokens);

  const labels = sortedFileTypes.map((fileType) => fileType.extension);
  const data = sortedFileTypes.map((fileType) => fileType.tokens);

  const chartData = {
    labels: labels,
    datasets: [
      {
        data: data,
        backgroundColor: [
          "#36A2EB",
          "#4BC0C0",
          "#FFCE56",
          "#FF6384",
          "#FF9F40",
          "#9966FF",
          "#FF6384",
          "#FFCE56",
          "#4BC0C0",
          "#36A2EB",
        ],
      },
    ],
  };

  const options = {
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: (context: TooltipItem<"pie">) => {
            const fileType = sortedFileTypes[context.dataIndex];
            if (!fileType) return [];

            const totalTokens = data.reduce((a, b) => a + b, 0);
            const percentage = ((fileType.tokens / totalTokens) * 100).toFixed(
              1
            );

            return [
              `${fileType.tokens.toLocaleString()} tokens (${percentage}%)`,
            ];
          },
        },
      },
    },
  };

  return (
    <Card className="shadow-md rounded-lg p-2">
      <CardHeader className="p-4">
        <CardTitle>Context length distribution by file type</CardTitle>
        <CardDescription>
          Total context length for each file type, sorted by size
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="chart-container">
          <Pie data={chartData} options={options} />
        </div>
      </CardContent>
    </Card>
  );
}

export { FileTypesChart };
