import { FileTypesChart } from "./file-types-chart";
import { DigestStatistics } from "./digest-statistics";
import { TopFilesChart } from "./top-files-chart";
import { AllFilesTable } from "./all-files-table";
import { Summary } from "@/types";
interface ReportParams {
  summary: Summary;
  author: string;
  name: string;
}

function Report({ summary, author, name }: ReportParams) {
  const { fileTypes, fileData } = summary;

  return (
    <div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        <FileTypesChart fileTypes={fileTypes} />
        <DigestStatistics summary={summary} />
      </div>

      <TopFilesChart fileData={fileData} />
      <AllFilesTable fileData={fileData} author={author} name={name} />
    </div>
  );
}

export { Report };
