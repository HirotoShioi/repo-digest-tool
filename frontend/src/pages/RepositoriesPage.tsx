import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Plus } from "lucide-react";
import { SearchFilter } from "@/components/SearchFilter";
import { AddRepositoryDialog } from "@/components/AddRepositoryDialog";
import { RepositoryList } from "@/components/RepositoryList";
import { useRepositories } from "@/hooks/useRepositories";
import { Repository } from "@/types";

export function RepositoriesPage() {
  const navigate = useNavigate();
  const { repositories, addRepository, deleteRepository, updateRepository } =
    useRepositories();
  const [searchQuery, setSearchQuery] = useState("");
  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false);

  const filteredRepositories = repositories.filter(
    (repo) =>
      repo.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      repo.url.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleSelectRepository = (repository: Repository) => {
    navigate(`/repository/${repository.id}`);
  };

  return (
    <div>
      <div className="flex items-center gap-4 mb-6">
        <div className="flex-1">
          <SearchFilter value={searchQuery} onChange={setSearchQuery} />
        </div>
        <button
          onClick={() => setIsAddDialogOpen(true)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          <Plus className="w-5 h-5" />
          Add Repository
        </button>
      </div>

      <RepositoryList
        repositories={filteredRepositories}
        selectedRepo={null}
        onDelete={deleteRepository}
        onUpdate={updateRepository}
        onSelect={handleSelectRepository}
      />

      <AddRepositoryDialog
        isOpen={isAddDialogOpen}
        onClose={() => setIsAddDialogOpen(false)}
        onAdd={addRepository}
      />
    </div>
  );
}
