import FileTypesChart from "./FileTypesChart";
import DigestStatistics from "./DigestStatistics";
import TopFilesChart from "./TopFilesChart";
import AllFilesTable from "./AllFilesTable";
import { Summary } from "@/types";
import { FileText } from "lucide-react";

interface ReportParams {
  summary: Summary;
}

function Report({ summary }: ReportParams) {
  const {
    repository,
    fileTypes,
    fileData,
  } = summary;

  return (
    <div>
      {/* Header */}
      <h1 className="text-2xl font-bold mb-4 flex items-center gap-2">
        <FileText className="w-6 h-6" />
        {repository}
      </h1>

      {/* File Types Distribution & Digest Statistics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        <FileTypesChart fileTypes={fileTypes} />
        <DigestStatistics summary={summary} />
      </div>

      <TopFilesChart fileData={fileData} />
      <AllFilesTable fileData={fileData} />
    </div>
  );
}

export default Report;
