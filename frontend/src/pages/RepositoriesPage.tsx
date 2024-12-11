import { useState } from "react";
import { useNavigate } from "react-router";
import { Plus } from "lucide-react";
import { AddRepositoryDialog } from "@/components/AddRepositoryDialog";
import { RepositoryList } from "@/components/RepositoryList";
import { useRepositories } from "@/hooks/useRepositories";
import { Repository } from "@/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

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
    navigate(`/repository/${repository.author}/${repository.name}`);
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-4">
        <div className="flex-1 justify-center items-center">
          <Input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search repositories..."
          />
        </div>
        <Button
          onClick={() => setIsAddDialogOpen(true)}
          className="bg-green-700 hover:bg-green-800"
        >
          <Plus className="w-5 h-5" />
          Add Repository
        </Button>
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
