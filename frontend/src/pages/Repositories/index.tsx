import { useState } from "react";
import { AddRepositoryDialog } from "@/pages/Repositories/components/AddRepositoryDialog";
import { RepositoryList } from "@/pages/Repositories/components/RepositoryList";
import { Input } from "@/components/ui/input";
import { useGetRepositories } from "@/services/repositories/queries";
import { LoadingSpinner } from "@/components/LoadingSpinner";
import { Search } from "lucide-react";
import React from "react";

function RepositoriesPage() {
  const { data: repositories, isLoading } = useGetRepositories();
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

      {isLoading ? (
        <LoadingSpinner size={48} minHeight={500} />
      ) : (
        <RepositoryList repositories={filteredRepositories} />
      )}
    </div>
  );
}

export default RepositoriesPage;
