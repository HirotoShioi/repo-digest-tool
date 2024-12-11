import type { Repository } from "../types";
import { RepositoryCard } from "./RepositoryCard";

interface RepositoryListProps {
  repositories: Repository[];
  selectedRepo: Repository | null;
  onSelect: (repository: Repository) => void;
}

export function RepositoryList({
  repositories,
  selectedRepo,
  onSelect,
}: RepositoryListProps) {
  return (
    <div className="space-y-4">
      {repositories.map((repo) => (
        <RepositoryCard
          key={repo.id}
          repository={repo}
          onSelect={onSelect}
          isSelected={selectedRepo?.id === repo.id}
        />
      ))}
      {repositories.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No repositories added yet. Add one using the form above.
        </div>
      )}
    </div>
  );
}