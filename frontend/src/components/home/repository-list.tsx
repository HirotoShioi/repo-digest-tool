import { Link } from "@tanstack/react-router";
import type { Repository } from "../../types";
import { RepositoryCard } from "./repository-card";

interface RepositoryListProps {
  repositories: Repository[];
}

export function RepositoryList({ repositories }: RepositoryListProps) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-4">
      {repositories.map((repo) => (
        <Link
          to={"/$author/$name"}
          params={{
            author: repo.author,
            name: repo.name,
          }}
        >
          <RepositoryCard repository={repo} key={repo.id} />
        </Link>
      ))}
      {repositories.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No repositories added yet. Add one using the form above.
        </div>
      )}
    </div>
  );
}
