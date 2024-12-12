import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card";

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
    <Card className="bg-white shadow-md rounded-lg p-2">
      <CardHeader className="p-4">
        <CardTitle>Context length distribution by file type</CardTitle>
        <CardDescription>
          Total context length for each file type, sorted by size
        </CardDescription>
      </CardHeader>
      <CardContent>
      <div className="chart-container">
        <Pie data={chartData} />
      </div>
      </CardContent>
    </Card>
  );
}

export default FileTypesChart;
