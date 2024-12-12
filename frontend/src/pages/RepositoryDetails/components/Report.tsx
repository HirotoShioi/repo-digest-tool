import FileTypesChart from "./FileTypesChart";
import DigestStatistics from "./DigestStatistics";
import TopFilesChart from "./TopFilesChart";
import AllFilesTable from "./AllFilesTable";
import { Summary } from "@/types";
import { FileText, Settings } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { SettingDialog } from "./SettingDialog";

interface ReportParams {
  summary: Summary;
}

function Report({ summary }: ReportParams) {
  const [open, setOpen] = useState(false);
  const {
    repository,
    fileTypes,
    fileData,
  } = summary;

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <FileText className="w-6 h-6" />
          {repository}
        </h1>
        <Button variant="outline" size="sm" onClick={() => setOpen(true)}>
          <Settings className="w-4 h-4 mr-2" />
          Settings
        </Button>
      </div>

      {/* File Types Distribution & Digest Statistics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        <FileTypesChart fileTypes={fileTypes} />
        <DigestStatistics summary={summary} />
      </div>

      <TopFilesChart fileData={fileData} />
      <AllFilesTable fileData={fileData} />
      <SettingDialog open={open} onOpenChange={setOpen} />
    </div>
  );
}

export default Report;
