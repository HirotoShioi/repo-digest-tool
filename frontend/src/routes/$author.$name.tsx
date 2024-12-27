import {
  createFileRoute,
  useNavigate,
  useParams,
} from "@tanstack/react-router";
import { useGetSummary } from "@/services/summary/queries";
import { Report } from "@/components/repository-info/statistics";
import { Download, FileText } from "lucide-react";
import { FilterSettingDialog } from "@/components/repository-info/filter-setting-dialog";
import { LoadingSpinner } from "@/components/loading-spinner";
import { useGenerateDigest } from "@/services/digest/mutations";
import { LoadingButton } from "@/components/loading-button";
import React, { useEffect } from "react";
import { useToast } from "@/hooks/use-toast";
import { queryOptions, useSuspenseQuery } from "@tanstack/react-query";
import { getRepositoryById } from "@/services/repositories/service";

type GetRepositoryQueryOptionsParams = {
  author: string;
  name: string;
};

function getRepositoryQueryOptions({
  author,
  name,
}: GetRepositoryQueryOptionsParams) {
  return queryOptions({
    queryKey: ["repository", author, name],
    queryFn: async () => getRepositoryById({ author, name }),
  });
}

export const Route = createFileRoute("/$author/$name")({
  loader: (opts) => {
    opts.context.queryClient.ensureQueryData(
      getRepositoryQueryOptions({
        author: opts.params.author,
        name: opts.params.name,
      })
    );
  },
  component: RouteComponent,
  notFoundComponent: () => <div>Repository not found</div>,
});

function RouteComponent() {
  const { author, name } = useParams({
    from: "/$author/$name",
  });
  const navigate = useNavigate();
  const {
    data: repository,
    isLoading,
    error,
  } = useSuspenseQuery(
    getRepositoryQueryOptions({
      author: author,
      name: name,
    })
  );
  const { toast } = useToast();

  useEffect(() => {
    if (error) {
      toast({
        title: "Error",
        description: "Failed to fetch repository. Please try again later.",
        variant: "destructive",
      });
    }
  }, [error, toast]);

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
          onClick={() => navigate({ to: "/" })}
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
