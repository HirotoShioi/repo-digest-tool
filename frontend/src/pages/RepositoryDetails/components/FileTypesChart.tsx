import { Pie } from "react-chartjs-2";

type FileTypeAggregation = {
    extension: string;
    count: number;
    tokens: number;
};


interface FileTypesChartParams {
    fileTypes: FileTypeAggregation[];
}


function FileTypesChart({ fileTypes }: FileTypesChartParams) {
    const labels = fileTypes.map(fileType => fileType.extension);
    const data = fileTypes.map(fileType => fileType.tokens);

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
        (Total context length for each file type)
      </span>
      <div className="chart-container">
        <Pie data={chartData} />
      </div>
    </div>
  );
};

export default FileTypesChart;