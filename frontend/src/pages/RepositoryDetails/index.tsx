import { useParams, useNavigate } from "react-router";
import { useGetRepositoryById } from "@/services/repositories/queries";
import { useGetSummary } from "@/services/summary/queries";
import Report from "./components/Report";
import { Button } from "@/components/ui/button";
import { Download, FileText, Settings } from "lucide-react";
import { useState } from "react";
import { FilterSettingDialog } from "./components/FilterSettingDialog";
import { LoadingSpinner } from "../../components/LoadingSpinner";
import { useGenerateDigest } from "@/services/digest/mutations";
import { LoadingButton } from "@/components/LoadingButton";

function RepositoryDetailsPage() {
  const { author, name } = useParams<{ author: string; name: string }>();
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();
  const { data: repository, isLoading } = useGetRepositoryById({
    author: author,
    name: name,
  });
  const {
    data: summary,
    refetch,
    isLoading: isSummaryLoading,
    isFetching,
  } = useGetSummary({
    author: author,
    repositoryName: name,
  });

  const { mutate: generateDigest, isPending: isDigestLoading } =
    useGenerateDigest();

  if (!author || !name) {
    return <div>Repository not found</div>;
  }

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
        <div className="flex gap-2 flex-col">
          <h1 className="text-2xl font-bold flex items-center gap-2">
            <FileText className="w-6 h-6" />
            {repository.name}
          </h1>
          <a
            href={repository.url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-muted-foreground"
          >
            {repository.url}
          </a>
        </div>
        <div className="flex items-center gap-2">
          <LoadingButton
            isLoading={isDigestLoading}
            variant="outline"
            loadingText="Generating..."
            onClick={() => generateDigest({ author, repositoryName: name })}
          >
            <Download className="w-4 h-4" />
            Get Digest
          </LoadingButton>
          <Button
            size="lg"
            onClick={() => setOpen(true)}
            className="bg-primary hover:bg-primary/90"
          >
            <Settings className="w-4 h-4" />
            Filter
          </Button>
          <FilterSettingDialog
            open={open}
            onOpenChange={setOpen}
            onSave={() => {
              refetch({});
            }}
          />
        </div>
      </div>
      {isFetching && !isSummaryLoading ? (
        <LoadingSpinner
          minHeight={500}
          size={48}
          label="Updating digest summary..."
        />
      ) : isSummaryLoading ? (
        <LoadingSpinner
          minHeight={500}
          size={48}
          label="Loading digest summary..."
        />
      ) : summary ? (
        <Report summary={summary} />
      ) : (
        <div className="text-center py-8 text-gray-600">
          No analysis data available
        </div>
      )}
    </>
  );
}

export default RepositoryDetailsPage;
