import React from "react";
import FileTypesChart from "./FileTypesChart";
import DigestStatistics from "./DigestStatistics";
import TopFilesChart from "./TopFilesChart";
import AllFilesTable from "./AllFilesTable";

interface ReportData {
    repo_name: string;
    summary: {
        contextLength: number;
        totalFiles: number;
        totalSizeKb: number;
        averageFileSizeKb: number;
        maxFileSizeKb: number;
        minFileSizeKb: number;
    };
    fileTypesLabels: string[];
    fileTypesData: number[];
    fileSizesLabels: string[];
    fileSizesData: number[];
    allFiles: {
        name: string;
        path: string;
        tokens: number;
    }[];
}

interface ReportParams {
    reportData: ReportData;
}

const Report: React.FC<ReportParams> = ({ reportData }) => {
  const {
    repo_name,
    summary,
    fileTypesLabels,
    fileTypesData,
    fileSizesLabels,
    fileSizesData,
    allFiles,
  } = reportData;


  return (
    <div className="container mx-auto p-6">
      {/* Header */}
      <h1 className="text-4xl font-bold text-center mb-8">
        Repository Digest Report - {repo_name}
      </h1>

      {/* File Types Distribution & Digest Statistics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        <FileTypesChart labels={fileTypesLabels} data={fileTypesData} />
        <DigestStatistics summary={summary} />
      </div>

      <TopFilesChart
        labels={fileSizesLabels}
        data={fileSizesData}
      />
      <AllFilesTable allFiles={allFiles} />
    </div>
  );
};

export default Report;