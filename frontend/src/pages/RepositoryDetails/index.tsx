import { useParams, useNavigate } from "react-router";
import { useGetRepositoryById } from "@/services/repositories/queries";
import { useGetSummary } from "@/services/summary/queries";
import Report from "./components/Report";
import { Button } from "@/components/ui/button";
import { FileText, Settings } from "lucide-react";
import { useState } from "react";
import { FilterSettingDialog } from "./components/FilterSettingDialog";

function RepositoryDetailsPage() {
  const { author, name } = useParams<{ author: string; name: string }>();
  if (!author || !name) {
    return <div>Repository not found</div>;
  }
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();
  const { data: repository, isLoading } = useGetRepositoryById({
    author,
    name,
  });
  const { data: summary, refetch, isLoading: isSummaryLoading } = useGetSummary({
    author,
    repositoryName: name,
  });

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!repository) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">Repository not found</p>
        <button
          onClick={() => navigate("/")}
          className="mt-4 text-blue-600 hover:text-blue-800"
        >
          Return to repository list
        </button>
      </div>
    );
  }

  return (
    <>
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <FileText className="w-6 h-6" />
          {repository.name}
        </h1>
        <Button size="lg" onClick={() => setOpen(true)} className="bg-green-600 hover:bg-green-700">
          <Settings className="w-4 h-4" />
          Filter
        </Button>
        <FilterSettingDialog open={open} onOpenChange={setOpen} onSave={() => {
          refetch({
            
          });
        }} />
      </div>
      {summary && !isSummaryLoading ? (
        <Report summary={summary} />
      ) : (
        <div>Loading...</div>
      )}
    </>
  );
}

export default RepositoryDetailsPage;
