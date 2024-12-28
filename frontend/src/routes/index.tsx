import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { AddRepositoryDialog } from "@/components/home/add-repository-dialog";
import { RepositoryList } from "@/components/home/repository-list";
import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";
import React from "react";
import { getRepositories } from "@/services/repositories/service";
import { queryOptions, useSuspenseQuery } from "@tanstack/react-query";

const getRepositoryQueryOptions = () => {
  return queryOptions({
    queryKey: ["repositories"],
    queryFn: async () => {
      return getRepositories();
    },
  });
};

export const Route = createFileRoute("/")({
  loader: (opts) => {
    opts.context.queryClient.ensureQueryData(getRepositoryQueryOptions());
  },
  component: RouteComponent,
});

function RouteComponent() {
  const { data: repositories } = useSuspenseQuery(getRepositoryQueryOptions());
  const [searchQuery, setSearchQuery] = useState("");
  const AddRepository = React.memo(AddRepositoryDialog);

  const filteredRepositories = (repositories ?? [])
    .filter(
      (repo) =>
        repo.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        repo.url.toLowerCase().includes(searchQuery.toLowerCase())
    )
    .sort((a, b) => a.name.localeCompare(b.name));

  return (
    <div className="space-y-8">
      <div className="flex items-center gap-4">
        <div className="flex-1 justify-center items-center relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
          <Input
            type="text"
            className="w-full border-primary pl-9"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search repositories..."
          />
        </div>
        <AddRepository />
      </div>

      <RepositoryList repositories={filteredRepositories} />
    </div>
  );
}
