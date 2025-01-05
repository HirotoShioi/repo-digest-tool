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
import React from "react";
import { useSuspenseQueries } from "@tanstack/react-query";
import { z } from "zod";
import { getRepositoryByIdQueryOptions } from "@/services/repositories/queries";
import { getSettingsQueryOptions } from "@/services/settings/queries";

export const Route = createFileRoute("/$author/$name")({
  params: {
    parse: (params) => ({
      author: z.string().parse(params.author),
      name: z.string().parse(params.name),
    }),
  },
  loader: async (opts) => {
    await opts.context.queryClient.ensureQueryData(
      getRepositoryByIdQueryOptions({
        author: opts.params.author,
        name: opts.params.name,
      })
    );
    await opts.context.queryClient.ensureQueryData(
      getSettingsQueryOptions({
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
  const [{ data: repository }, { data: settings }] = useSuspenseQueries({
    queries: [
      getRepositoryByIdQueryOptions({
        author: author,
        name: name,
      }),
      getSettingsQueryOptions({
        author: author,
        name: name,
      }),
    ],
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

  if (!repository || !settings) {
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
            settings={settings}
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
