import { useParams, useNavigate } from "react-router";
import { useGetRepositoryById } from "@/services/repositories/queries";
import { useGetSummary } from "@/services/summary/queries";
import Report from "./components/Report";
import { Download, FileText } from "lucide-react";
import { FilterSettingDialog } from "./components/FilterSettingDialog";
import { LoadingSpinner } from "../../components/LoadingSpinner";
import { useGenerateDigest } from "@/services/digest/mutations";
import { LoadingButton } from "@/components/LoadingButton";
import React from "react";

function RepositoryDetailsPage() {
  const { author, name } = useParams<{ author: string; name: string }>();
  const navigate = useNavigate();
  const { data: repository, isLoading } = useGetRepositoryById({
    author: author,
    name: name,
  });
  const FilterDialog = React.memo(FilterSettingDialog);
  const {
    data: summary,
    refetch,
    isLoading: isSummaryLoading,
    isFetching,
  } = useGetSummary({
    author: author,
    name: name,
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
          <FilterDialog
            onSave={() => {
              refetch({});
            }}
            author={author}
            repository={name}
          />
        </div>
      </div>
      {isFetching && !isSummaryLoading && (
        <div className="fixed inset-0 bg-background/80 backdrop-blur-sm z-50 flex items-center justify-center">
          <LoadingSpinner size={48} label="Updating digest summary..." />
        </div>
      )}
      {isSummaryLoading ? (
        <LoadingSpinner
          minHeight={500}
          size={48}
          label="Loading digest summary..."
        />
      ) : summary ? (
        <Report summary={summary} author={author} name={name} />
      ) : (
        <div className="text-center py-8 text-gray-600">
          No analysis data available
        </div>
      )}
    </>
  );
}

export default RepositoryDetailsPage;
