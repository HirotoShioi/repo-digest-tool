import { useState } from "react";
import { Plus } from "lucide-react";
import { AddRepositoryDialog } from "@/pages/Repositories/components/AddRepositoryDialog";
import { RepositoryList } from "@/pages/Repositories/components/RepositoryList";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useGetRepositories } from "@/services/repositories/queries";

function RepositoriesPage() {
  const { data: repositories } = useGetRepositories();
  const [searchQuery, setSearchQuery] = useState("");
  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false);

  const filteredRepositories = repositories.filter(
    (repo) =>
      repo.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      repo.url.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-8">
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
      />

      <AddRepositoryDialog
        isOpen={isAddDialogOpen}
        onClose={() => setIsAddDialogOpen(false)}
      />
    </div>
  );
}

export default RepositoriesPage;
