import FileTypesChart from "./FileTypesChart";
import DigestStatistics from "./DigestStatistics";
import TopFilesChart from "./TopFilesChart";
import AllFilesTable from "./AllFilesTable";
import { Summary } from "@/types";
interface ReportParams {
  summary: Summary;
}

function Report({ summary}: ReportParams) {
  const {
    repository,
    fileTypes,
    fileData,
  } = summary;

  return (
    <div>
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
